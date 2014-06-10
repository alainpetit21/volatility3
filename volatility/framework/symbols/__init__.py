'''
Created on 7 Feb 2013

@author: mike
'''

import collections

from volatility.framework import objects, interfaces, exceptions


class SymbolSpace(collections.Mapping):
    """Handles an ordered collection of SymbolTables

       This collection is ordered so that resolution of symbols can
       proceed down through the ranks if a namespace isn't specified.
    """

    def __init__(self, native_structures):
        if not isinstance(native_structures, interfaces.symbols.NativeTableInterface):
            raise TypeError("SymbolSpace native_structures must be NativeSymbolInterface")
        self._dict = collections.OrderedDict()
        self._native_structures = native_structures
        # Permanently cache all resolved symbols
        self._resolved = {}

    @property
    def natives(self):
        """Returns the native_types for this symbol space"""
        return self._native_structures

    def __len__(self):
        return len(self._dict)

    def __getitem__(self, i):
        return self._dict[i]

    def __iter__(self):
        return self._dict.__iter__()

    def append(self, value):
        """Adds a symbol_list to the end of the space"""
        if not isinstance(value, interfaces.symbols.SymbolTableInterface):
            raise TypeError(value)
        if value.name in self._dict:
            self.remove(value.name)
        self._dict[value.name] = value

    def remove(self, key):
        """Removes a named symbol_list from the space"""
        # Reset the resolved list, since we're removing some symbols
        self._resolved = {}
        del self._dict[key]

    def _weak_resolve(self, symbol):
        """Takes a symbol name and resolves it with ReferentialTemplates"""
        symarr = symbol.split("!")
        if len(symarr) == 2:
            table_name = symarr[0]
            structure_name = symarr[1]
            return self._dict[table_name].get_structure(structure_name)
        elif symbol in self.natives.structures:
            return self.natives.get_structure(symbol)
        raise exceptions.SymbolError("Malformed symbol name")

    def get_structure(self, symbol):
        """Takes a symbol name and resolves it

           This method ensures that all referenced templates (including self-referential templates)
           are satisfied as ObjectTemplates
        """
        # Traverse down any resolutions
        if symbol not in self._resolved:
            self._resolved[symbol] = self._weak_resolve(symbol)
            traverse_list = [symbol]
            replacements = set()
            # Whole Symbols that still need traversing
            while traverse_list:
                template_traverse_list, traverse_list = [self._resolved[traverse_list[0]]], traverse_list[1:]
                # Traverse a single symbol looking for any ReferenceTemplate objects
                while template_traverse_list:
                    traverser, template_traverse_list = template_traverse_list[0], template_traverse_list[1:]
                    for child in traverser.children:
                        if isinstance(child, objects.templates.ReferenceTemplate):
                            # If we haven't seen it before, subresolve it and also add it
                            # to the "symbols that still need traversing" list
                            if child.structure_name not in self._resolved:
                                traverse_list.append(child.structure_name)
                                self._resolved[child.structure_name] = self._weak_resolve(child.structure_name)
                            # Stash the replacement
                            replacements.add((traverser, child))
                        elif child.children:
                            template_traverse_list.append(child)
            for (parent, child) in replacements:
                parent.replace_child(child, self._resolved[child.structure_name])
        return self._resolved[symbol]

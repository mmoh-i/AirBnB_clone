#!/usr/bin/python3

import cmd
import json
from models.base_model import BaseModel
from models import storage
import re


class HBNBCommand(cmd.Cmd):

    prompt = '(hbnb)'

    def default(self, line):
        """Track if nothing else mathch"""
        self._precmd(line)

    def do_create(self, line):
        """Creates a new instance of BaseModel"""
        if line == "" or line is None:
            print("** class name missing **")
        elif line not in storage.classes():
            print("** class dosen't exist **")
        else:
            b = storage.classes()[line]()
            b.save()
            print(b.id)

    def do_show(self, line):
        """Prints the string repr of an instnce"""
        if line == "" or line is None:
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class dosen't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(words[0], words[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])

    def do_destroy(self, line):
        if line == "" or line is None:
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class dosen't exist **")
            elif words[1] == " " or words[1] is None:
                print("** instance id  missing **")
            else:
                key = "{}.{}".format(words[0], words[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()

    def do_all(self, line):
        if line == "" or line is None:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class dosen't exist **")
            else:
                s = [str(v) for k, v in storage.all().items()\
                        if type(v).__name__ == words[0]]
        else:
            print([str(v) for k, v in storage.all().items()])

    def do_update(self, line):
        if line == "" or line is None:
            print("** class name missing **")
            return

        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(rex, line)
        classname = match.group(1)
        uid = match.group(2)
        attribute = match.group(3)
        value = match.group(4)
        if not match:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                cast = None
                if not re.search('^".*"$', value):
                    if '.' in value:
                        cast = float
                    else:
                        cast = int
                else:
                    value = value.replace('"', '')
                attributes = storage.attributes()[classname]
                if attribute in attributes:
                    value = attributes[attribute](value)
                elif cast:
                    try:
                        value = cast(value)
                    except ValueError:
                        pass  # fine, stay a string then
                setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()

    def do_EOF(self, line):
        """EOF to End Of File"""
        print()
        return True

    def do_quit(self, line):
        """To Exit the program"""
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()

#!/usr/bin/python3
""" main program executable """

import cmd
import json
from models.base_model import BaseModel
import models.base_model
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ command interpreter """

    prompt = '(hbnb)'

    def emptyline(self):
        """ override emptyline func """
        pass

    def onecmd(self, arg):
        """ overrride onecmd func """
        return cmd.Cmd.onecmd(self, arg)

    def precmd(self, line):
        """ parse line for cmd & args """
        pos_double_quote, pos_period = line.find('"'), line.find('.')

        if pos_period == -1:
            return line

        if pos_double_quote != -1 and pos_double_quote < pos_period:
            return line

        new_line = parse(line)
        return new_line

    def do_quit(self, arg):
        """ Close """
        exit()

    def help_quit(self):
        """ quit help """
        print("Quit command to exit program\n")

    def do_EOF(self, arg):
        """ close """
        exit()

    def help_EOF(self):
        """ eof help """
        print("Quit command to exit program\n")

    def do_create(self, arg):
        """ create new instance """
        newObj = assignCls(arg)
        if newObj is None:
            return
        newObj.save()
        print(newObj.id)

    def help_create(self):
        """ create help """
        print("Create an instance of a class")
        print("Usage: create <class name>\n")

    def do_show(self, arg):
        """ prints string of an instance """
        name = condChk(arg)
        if name is None:
            return

        try:
            with open('file.json', 'r') as f:
                objDict = json.load(f)
        except:
            return

        if name not in objDict:
            print("** no instance found **")
            return
        kwarg = objDict[name]
        obj = assignCls(arg, kwarg)
        print(obj)
        del(obj)

    def help_show(self):
        """ show help """
        pass

    def do_destroy(self, arg):
        """ remove obj from JSON File """
        name = condChk(arg)
        if name is None:
            return
        try:
            with open('file.json', 'r') as f:
                objDict = json.load(f)
        except:
            return

        if name not in objDict:
            print("** no instance found **")
            return
        objDict.pop(name)
        with open('file.json', 'w') as f:
            objDict = json.dump(objDict, f, sort_keys=True, indent=4)

    def help_destroy(self):
        """ help destroy """
        pass

    def do_all(self, arg):
        """ show all objects """
        clsList = [
            'User', 'State', 'City',
            'Amenity', 'Place',
            'Review', 'BaseModel'
        ]
        empty = False
        if arg == "":
            empty = True
        elif arg not in clsList:
            print("** class doesn't exist **")
            return
        allList = []
        try:
            with open('file.json', 'r') as f:
                objDict = json.load(f)
        except:
            return

        for key in objDict:
            obj_class = objDict[key]["__class__"]
            if obj_class != arg \
                    and empty is False:
                continue
            obj = assignCls(obj_class, objDict[key])
            allList.append(str(obj))
            del(obj)
        print(allList)

    def help_all(self):
        """ show help """
        pass

    def do_update(self, arg):
        """ updates an object """
        name = condChk(arg)
        if name is None:
            return
        with open('file.json', 'r') as f:
            objDict = json.load(f)
        if name not in objDict:
            print("** no instance found **")
            return
        updateObj = arg.split(" ")
        length = len(updateObj)
        if length < 3:
            print("** attribute name missing **")
            return
        if length < 4:
            print("** value missing **")
            return
        attributeName = updateObj[2]

        updateObj.pop(2)
        updateObj.pop(1)
        class_name = updateObj.pop(0)
        value = ' '.join(updateObj).replace('"', '')

        newObj = assignCls(class_name, objDict[name])
        setattr(newObj, attributeName, value)
        newObj.save()
        del newObj

    def help_update(self):
        """ update help """
        pass


def assignCls(args, kwargs={}):
    """assigning class obj """

    arg_list = args.split(" ")
    arg = arg_list[0]

    if not arg:
        print("** class name missing **")
        return None
    clsList = [
        'User', 'State', 'City',
        'Amenity', 'Place',
        'Review', 'BaseModel'
    ]
    if arg == 'User':
        return User(**kwargs)
    if arg == 'State':
        return State(**kwargs)
    if arg == 'City':
        return City(**kwargs)
    if arg == 'Amenity':
        return Amenity(**kwargs)
    if arg == 'Place':
        return Place(**kwargs)
    if arg == 'Review':
        return Review(**kwargs)
    if arg == 'BaseModel':
        return BaseModel(**kwargs)
    if arg not in clsList:
        print("** class doesn't exist **")
        return None


def condChk(arg):
    """ checking on conditionals for obj """
    clsList = [
        'User', 'State', 'City',
        'Amenity', 'Place',
        'Review', 'BaseModel'
    ]
    argList = arg.split(" ")
    length = len(argList)
    if argList == [""]:
        print("** class name missing **")
        return None
    if argList[0] not in clsList:
        print("** class doesn't exist **")
        return None
    if length < 2:
        print("** instance id missing **")
        return None
    return argList[0] + "." + argList[1]


def parse(line):
    """ parse line for cmd & args """
    cmd_list = line.split('.')
    class_name = cmd_list[0]
    cmd_list = cmd_list[1].split('(')
    cmd = cmd_list[0]
    arg = cmd_list[1][:-1]

    arg_list = arg.split(', ')
    arg_list[0] = arg_list[0].replace('"', '')
    try:
        arg_list[1] = arg_list[1].replace('"', '')
    except:
        pass

    arg = " ".join(arg_list)
    cmd_list = [cmd, class_name, arg]
    new_line = " ".join(cmd_list)

    return (new_line)

if __name__ == '__main__':
    HBNBCommand().cmdloop()

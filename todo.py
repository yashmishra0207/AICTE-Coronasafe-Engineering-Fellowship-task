from datetime import datetime
import sys
import pytz


todoFile = 'todo.txt'
doneFile = 'done.txt'


# creating files for storing pending and completed todos
with open(todoFile, 'a') as file:
    pass
with open(doneFile, 'a') as file:
    pass


def run_app(command=None, *args):
    '''
    Takes in optional arguments from command line,
    performs actions as per various commands.
        Parameters:
            command (str): A command
            args (str): Additional argument
        Returns:
            void
    '''
    if command == 'help' or not command:
        show_help()
    else:
        commands = {
            'ls':     list_todo,
            'report': show_report
        }
        commandsWithArgs = {
            'add':    add_todo,
            'del':    delete_todo,
            'done':   mark_as_done,
            'insert': insert_at,
            'update': update_todo,
            'swap':   swap_todo
        }
        commands = commands.get(command, False)
        commandsWithArgs = commandsWithArgs.get(command, False)
        if not commands:
            if not commandsWithArgs:
                print('command not found!')
                sys.exit(0)
            else:
                commandsWithArgs(*args)
        else:
            commands()
                


def add_todo(newTodo=None):
    '''
    Takes in todo as string, adds it to the todos.
        Parameters:
            newTodo (str): String containing todo
        Returns:
            void
    '''
    if not newTodo:
        show_error('add')
    else:
        newTodo = newTodo.strip()
        oldTodo = None
        with open(todoFile, 'r') as file:
            oldTodo = file.read()
        with open(todoFile, 'w') as file: 
            if oldTodo:
                file.write(newTodo + '\n' + oldTodo)
            else:
                file.write(newTodo)
        print('Added todo: "{}"'.format(newTodo))


def insert_at(newTodo=None, position=None):
    '''
    Takes in todo and position as string, adds it to the todos at the given position.
        Parameters:
            newTodo (str): String containing todo
            position (str): String containing the position where new todo is to be inserted
        Returns:
            void
    '''
    if type(position) == type(str()):
        position = int(position.strip())
    if not newTodo:
        show_error('add')
    elif not position:
        show_error('insert')
    elif position < 1:
        show_error('invalid')
    else:
        todoCount = count_todo()
        if position > todoCount:
            add_todo(newTodo)
        else:
            oldTodos = ''
            if position == 1:
                with open(todoFile, 'a') as file:
                    file.write('\n' + newTodo)
            else:
                with open(todoFile, 'r') as file:
                    for idx, todo in enumerate(file):
                        if todoCount - idx == position:
                            oldTodos += (todo + newTodo + '\n')
                        else:
                            oldTodos += todo
                with open(todoFile, 'w') as file:
                    file.write(oldTodos)
            print('Added todo: "{}" at position {}'.format(newTodo, position))


def update_todo(updatedTodo=None, position=None):
    '''
    Takes in todo and position as string, it updates the todo at the given position.
        Parameters:
            newTodo (str): String containing todo
            position (str): String containing the position of todo to be udpated
        Returns:
            void
    '''
    if not updatedTodo:
        show_error('update')
    elif not position:
        show_error('insert')
    elif int(position.strip()) < 1:
        show_error('invalid')
    else:
        position = int(position.strip())
        todoCount = count_todo()
        if position > todoCount:
            show_error('missing_todo', position)
        else:
            oldTodos = ''
            toBeUpdated = ''
            with open(todoFile, 'r') as file:
                for idx, todo in enumerate(file):
                    if todoCount - idx == position:
                        toBeUpdated = todo
                        if position == 1:
                            oldTodos += (updatedTodo)
                        else:
                            oldTodos += (updatedTodo + '\n')
                    else:
                        oldTodos += todo
            with open(todoFile, 'w') as file:
                file.write(oldTodos)
            print('Updated todo: "{}" to "{}" at position {}'.format(toBeUpdated, updatedTodo, position))


def swap_todo(position1=None, position2=None):
    '''
    Takes in position1 and position2 as string, swaps the todos at given positions
        Parameters:
            position1 (str): String containing the position of first todo
            position2 (str): String containing the position of second todo
        Returns:
            void
    '''
    if position1 == None or position2 == None:
        show_error('swap')
    elif int(position1.strip()) < 1 or int(position2.strip()) < 1:
        show_error('invalid')
    else:
        position1, position2 = int(position1.strip()), int(position2.strip())
        todoCount = count_todo()
        if position1 > todoCount or position2 > todoCount:
            show_error('out_of_range', todoCount)
        elif position1 == position2:
            print('Nothing to swap!')
        else:
            position1, position2 = min(position1, position2), max(position1, position2)
            todo1 = remove_todo(position1)
            todo2 = remove_todo(position2 - 1)
            todo1 = todo1 if todo1[-2:] != '\n' else todo1[:-1]
            todo2 = todo2 if todo2[-2:] != '\n' else todo2[:-1]
            insert_at(todo1, position2 - 1)
            insert_at(todo2, position1)


def list_todo():
    '''
    Prints all the todos in reverse order of their insertion
        Parameters:
            no params required
        Returns:
            void
    '''
    todoCount= count_todo()
    if todoCount:
        with open(todoFile, 'r') as file:
            for idx, todo in enumerate(file):
                print('[{}] {}'.format(todoCount-idx, todo), end='')
        print()
    else:
        print('There are no pending todos!')


def delete_todo(toBeDeleted=None):
    '''
    Takes in todo number, removes the todo with entered todo number.
        Parameters:
            toBeDeleted (str): String containing todo number
        Returns:
            void
    '''
    if not toBeDeleted:
        show_error('delete')
    else:
        toBeDeleted = int(toBeDeleted.strip())
        todoCount = count_todo()
        if toBeDeleted > todoCount or toBeDeleted <= 0:
            show_error('missing_delete', toBeDeleted)
        else:
            remove_todo(toBeDeleted)
            print('Deleted todo #{}'.format(toBeDeleted))


def mark_as_done(toBeMarked=None):
    '''
    Takes in todo number, marks the todo with entered todo number as done and store it in the list of completed todos.
        Parameters:
            toBeMarked (str): String containing todo number
        Returns:
            void
    '''
    if len(args) == 2:
        show_error('todo')
    else:
        toBeMarked = int(toBeMarked.strip())
        todoCount = count_todo()
        if toBeMarked > todoCount or toBeMarked <= 0:
            show_error('missing_todo', toBeMarked)
        else:
            markedTodo = remove_todo(toBeMarked)
            newCompletion = 'x ' + get_current_date() + ' ' + markedTodo
            oldCompletions = None
            with open(doneFile, 'r') as file:
                oldCompletions = file.read()
            with open(doneFile, 'w') as file:
                if oldCompletions:
                    file.write(newCompletion + oldCompletions)
                else:
                    file.write(newCompletion)
            print('Marked todo #{} as done.'.format(toBeMarked))


def show_report():
    '''
    Prints the number of pending and completed todos.
        Parameters:
            no params
        Returns:
            void
    '''
    pending = count_todo()
    done = count_done()
    today = get_current_date()
    print("{} Pending : {} Completed : {}".format(today, pending, done))


def count_todo():
    '''
    Returns the number of todos left.
        Parameters:
            no params
        Returns:
            count (int): Number of todos left
    '''
    with open(todoFile, 'r') as file:
        count = 0
        while file.readline():
            count += 1
        return count


def count_done():
    '''
    Returns the number of todos completed.
        Parameters:
            no params    
        Returns:
            count (int): Number of todos completed
    '''
    with open(doneFile, 'r') as file:
        count = 0
        while file.readline():
            count += 1
        return count


def remove_todo(toBeRemoved=None):
    '''
    Takes in todo number, removes the todo with entered todo number and returns it.
        Parameters:
            toBeRemoved (str): String containing todo number
        Returns:
            removedTodo (str): String containing removed todo
    '''
    totalTodo = count_todo()
    currentTodo = None
    leftTodos = ''
    removedTodo = ''
    with open(todoFile, 'r') as file:
        for idx, todo in enumerate(file):
            currentTodo = totalTodo - idx
            if currentTodo != toBeRemoved:
                leftTodos += todo
            else:
                removedTodo = todo
    if toBeRemoved == 1:
        leftTodos = leftTodos[:-1]
    else:
        removedTodo = removedTodo[:-1]
    with open(todoFile, 'w') as file:
        file.write(leftTodos)
    return removedTodo


def get_current_date():
    '''
    Returns the current date in UTC format.
        Parameters:
            no params
        Returns:
            today (str): current date(UTC)
    '''
    today = datetime.now()
    today = today.astimezone(pytz.utc).strftime('%Y-%m-%d')
    return today

    
def show_error(errType, todoNumber=None):
    '''
    Takes in error type and optional todoNumber, prints the error as per the error type and todoNumber causing the error (if in case) 
        Parameters:
            errType (str): String containing error Type
            todoNumber (str): String containing erronious todoNumber
        Returns:
            void
    '''
    errors = {
        'add': 'Error: Missing todo string. Nothing added!',
        'update': 'Error: Missing udpated todo string. Nothing updated!',
        'delete': 'Error: Missing NUMBER for deleting todo.',
        'insert': 'Error: Missing argument for position.',
        'swap': 'Error: Expects 2 arguments for position.',
        'invalid': 'Error: Invalid position, must be greater than 0.',
        'missing_delete': 'Error: todo #{} does not exist. Nothing deleted.',
        'missing_todo': 'Error: todo #{} does not exist.',
        'out_of_range': 'Error: Position should be from 1 to {}.',
        'todo': 'Error: Missing NUMBER for marking todo as done.' 
    }
    error = errors.get(errType, 'an unknown error occured!')
    if todoNumber == None:
        print(error)
    else:
        print(error.format(todoNumber))
    

def show_help():
    '''
    Prints the help regarding the usage of various commands.
        Parameters:
            no params
        Returns:
            void
    '''
    print('Usage :-')
    print('$ ./todo add "todo item"                 # Add a new todo')
    print('$ ./todo insert "todo item" NUMBER       # Insert at a given position')
    print('$ ./todo update "todo item" NUMBER       # Update at a given position')
    print('$ ./todo swap NUMBER NUMBER              # Swap given todos')
    print('$ ./todo ls                              # Show remaining todos')
    print('$ ./todo del NUMBER                      # Delete a todo')
    print('$ ./todo done NUMBER                     # Complete a todo')
    print('$ ./todo help                            # Show usage')
    print('$ ./todo report                          # Statistics')


if __name__ == '__main__':
    args = sys.argv
    run_app(*args[1:])

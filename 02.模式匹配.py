args = ['gcc', 'hello.222c', 'world.c']

if args == ['gcc']:
    print('gcc: missing source file(s).')
elif len(args) >= 2 and args[0] == 'gcc':
    file1 = args[1]
    files = args[2:]
    print('gcc compile: ' + file1 + ', ' + ', '.join(files))
elif args == ['clean']:
    print('clean')
else:
    print('invalid command.')
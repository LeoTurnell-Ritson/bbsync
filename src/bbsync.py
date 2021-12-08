#!/usr/bin/env python3
#------------------------------------------------------------------------------
# =========                 |
# \\      /  F ield         | like rsync but for blue bear & OpenFOAM
#  \\    /   O peration     | Web: https://github.com/LeoTurnell-Ritson/bbsync
#   \\  /    A nd           |
#    \\/     M anipulation  |
#------------------------------------------------------------------------------

import sys
import os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='wrapper for shh/rsync for use with OpenFOAM and blue bear')
    parser.add_argument('--push', help='push from local to blue bear', nargs='+', required=False)
    parser.add_argument('--pull', help='pull files from blue bear to local', nargs='+', required=False)
    parser.add_argument('-a', '--absolute', help='use absolute path', required=False, action='store_true', default=False)
    parser.add_argument('-r', '--relative', help='use relative path (default)', required=False, action='store_true', default=False)
    parser.add_argument('-l', '--login', help='login to Blue Bear', required=False, action='store_true')
    parser.add_argument('-c', '--command', help='runs given terminal command on Blue Bear', required=False, nargs='+')
    parser.add_argument('-e', '--remote', help='bring up remote access webpage', required=False, action='store_true')
    parser.add_argument('-q', '--queue', help='print current sbatch queue', required=False, action='store_true')
    parser.add_argument('-v', '--verbose', help='print all commands run by bbsync, WARNING: may show passwords in plain text', required=False, action='store_true')

    args = vars(parser.parse_args())

    ## define ssh and rsync with args
    rsync = 'rsync -ru -e'
    ssh = 'ssh'

    ## get cwd
    cwd = os.getcwd()

    ## check prerequisite exports
    if  len(os.popen('printf $bbacc').read()) == 0:
        print(parser.prog + ': error: $bbacc not defined, to setup an account: export bbacc=\'user@bluebear.bham.ac.uk\'')
        sys.exit(1)
    else:
        bbacc = '%s' %(os.popen('printf $bbacc').read())

    if  len(os.popen('printf $bbproject').read()) == 0:
        print(parser.prog + ': error: $bbproject not defined, to setup a project: export bbproject=\'/rds/projects/2year/project_name\'')
        sys.exit(1)
    else:
        bbproject = '%s' %(os.popen('printf $bbproject').read())

    if  len(os.popen('printf $bbrun').read()) == 0:
        print(parser.prog + ': error: $bbrun not defined')
        sys.exit(1)
    else:
        bbrun = '%s' %(os.popen('printf $bbrun').read())

    if  len(os.popen('printf $bbapp').read()) == 0:
        print(parser.prog + ': error: $bbapp not defined')
        sys.exit(1)
    else:
        bbapp = '%s' %(os.popen('printf $bbapp').read())

    if  len(os.popen('printf $bbsrc').read()) == 0:
        print(parser.prog + ': error: $bbsrc not defined')
        sys.exit(1)
    else:
        bbsrc = '%s' %(os.popen('printf $bbsrc').read())

    ## key words
    key_dir = ['bbsync', 'src', 'applications']

    ## selecting path
    if args['absolute'] and args['relative']:
        print(parser.prog + ': error: cannot use both absolute and relative path')
        sys.exit(1)

    if args['absolute']:
        args['relative'] = False
    else:
        args['relative'] = True

    ## check if bbsync should use sshpass
    if len(os.popen('printf $bbpass').read()) == 0:
        ssh_pass = ''
    else:
        ssh_pass = 'sshpass -p %s' %(os.popen('printf $bbpass').read())

    ## extra helper functions
    if args['remote'] == True:
        os_command = 'google-chrome https://remoteaccess.bham.ac.uk/'
        if args['verbose']:
            print(os_command)
        os.system(os_command)

    if args['command'] != None:
        user_command = ' '.join(args['command'])
        os_command = '%s %s %s %s' %(ssh_pass, ssh, bbacc, user_command)
        if args['verbose']:
            print (os_command)
        os.system(os_command)

    if args['login'] == True:
        os_command = '%s %s %s' %(ssh_pass, ssh, bbacc)
        if args['verbose']:
            print (os_command)
        os.system(os_command)

    if args['queue'] == True:
        os_command = '%s %s %s %s' %(ssh_pass, ssh, bbacc, 'showq')
        if args['verbose']:
            print (os_command)
        os.system(os_command)

    ## push
    if args['push'] != None:
        for i in range(0, len(args['push'])):
            if args['relative']:
                local_path = cwd + '/' + args['push'][i]
            elif args['absolute']:
                local_path = args['push'][i]

            split_local_path = local_path.split('/')
            relative_bbpath = False

            for j in range(0, len(split_local_path)):
                if split_local_path[j] in key_dir:
                    if split_local_path[j] == 'bbsync':
                        in_path = '/'.join(split_local_path[j+1:])
                        bbpath = '%s:%s/%s/%s' %(bbacc, bbproject, bbrun, in_path)
                        relative_bbpath = True
                        break
                    elif split_local_path[j] == 'src':
                        in_path = '/'.join(split_local_path[j+1:])
                        bbpath = '%s:%s/%s/%s' %(bbacc, bbproject, bbsrc, in_path)
                        relative_bbpath = True
                        break
                    elif split_local_path[j] == 'applications':
                        in_path = '/'.join(split_local_path[j+1:])
                        bbpath = '%s:%s/%s/%s' %(bbacc, bbproject, bbapp, in_path)
                        relative_bbpath = True
                        break

            if relative_bbpath == False:
                print(parser.prog + ': warning: cannot find bbsync path for %s' %(local_path))
            else:
                os_command = '%s %s %s %s %s' %(ssh_pass, rsync, ssh, local_path, bbpath)
                if args['verbose']:
                    print (os_command)
                else:
                    print ('bbsync: %s %s' %(local_path, bbpath))
                os.system(os_command)

    ##pull
    if args['pull'] != None:
        for i in range(0, len(args['pull'])):
            if args['relative']:
                local_path = cwd + '/' + args['pull'][i]
            elif args['absolute']:
                local_path = args['pull'][i]

        split_local_path = local_path.split('/')
        relative_bbpath = False

        for j in range(0, len(split_local_path)):
            if split_local_path[j] in key_dir:
                if split_local_path[j] == 'bbsync':
                    in_path = '/'.join(split_local_path[j+1:])
                    bbpath = '%s:%s/%s/%s' %(bbacc, bbproject, bbrun, in_path)
                    relative_bbpath = True
                    break
                elif split_local_path[j] == 'src':
                    in_path = '/'.join(split_local_path[j+1:])
                    bbpath = '%s:%s/%s/%s' %(bbacc, bbproject, bbsrc, in_path)
                    relative_bbpath = True
                    break
                elif split_local_path[j] == 'applications':
                    in_path = '/'.join(split_local_path[j+1:])
                    bbpath = '%s:%s/%s/%s' %(bbacc, bbproject, bbapp, in_path)
                    relative_bbpath = True
                    break

        if relative_bbpath == False:
            print(parser.prog + ': warning: cannot find bbsync path for %s' %(local_path))
        else:
            os_command = '%s %s %s %s %s' %(ssh_pass, rsync, ssh, bbpath, local_path)
            if args['verbose']:
                print (os_command)
            else:
                print ('bbsync: %s %s' %(bbpath, local_path))
            os.system(os_command)

# ----------------------------------------------------------------- end-of-file

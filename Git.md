# Useful Git commands I always forget


## Pretty output 

git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit

## Searching the history 

git log -S 'StringToSearch'

git log --grep='StringToSearchInCommitMessages'

## Cleaning all branches 

git branch | grep -v "master" | xargs git branch -D

## Squash last commits 

git rebase -i HEAD~3

## Undo commits

git reset --hard HEAD~3  (can lose uncommitted modifications)

or 

git revert --no-commit HEAD~3

## Modify the last commit

git commit --amend 

In the future, the usual one-command update is:

git add . && git commit -m "update" && git push

This:

adds all changed files
commits them
uploads to GitHub

If GitHub changed too, first do:

git pull --rebase && git add . && git commit -m "update" && git push

For your own PC-only workflow, the first command is usually enough
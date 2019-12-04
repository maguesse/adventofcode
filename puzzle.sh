#!/usr/bin/env bash
self="${BASH_SOURCE[0]}"
selfdir="$(cd "$(dirname "${self}")";pwd)"
TMPL_DIR=${selfdir}/.tmpl
YEAR=2019
days=("" "one" "two" "three" "four" "five" "six"
"seven" "eight" "nine" "ten" "eleven" "twelve"
"thirteen" "fourteen" "fiveteen" "sixteen"
"seventeen" "heighteen" "nineteen"
"twenty" "twentyone" "twentytwo" "twentythree" "twentyfour" "twentyfive")

die() {
    echo "ERROR: $@"
    exit 1
}

usage() {
    cat <<EOF
Usage: ${0} action day [comment]

action:
    begin : creates a new branch and folder for the day
    save : Saves progression for the day
    end : Close the puzzle for the day
day: day to work on
comment: Save comment
EOF
}

branch_name() {
    echo ${YEAR}-day${days[$day]}
}

begin() {
    [[ -d ${DAY_FOLDER} ]] && die "Folder for day ${day} already exist!"
    check_branch "master"
    new_branch=$(branch_name)
    git checkout -b ${new_branch}
    mkdir -p ${DAY_FOLDER}
    cp ${TMPL_DIR}/main.py ${DAY_FOLDER}
    ln -s ${TMPL_DIR}/util.py ${DAY_FOLDER}
    git add ${DAY_FOLDER}
}

end() {
    old_branch=$(branch_name)
    check_branch ${old_branch}
    # Switch to master
    git checkout master || die "Unable to switch to master"
    # merge current to master
    git merge ${old_branch} || die "Unable to merge ${old_branch} to master"
    git push origin master || die "Unable to push master to remote"
    # Delete old branch
    git branch -d ${old_branch} || die "Unable to delete ${old_branch}"
    #git push origin --delete ${old_branch}
}


yes_no() {
    prompt=$1
    read -p "${prompt}? [y/N]: " CHOICE
    case ${CHOICE} in
        y|Y)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

add() {
    file=$1
    yes_no "Add $file" && git add ${file}
}

save() {
    bname=$(branch_name)
    check_branch ${bname}
    if [ $# -lt 1 ]; then
        usage
        exit
    fi
    comment=$1;shift
    comment="Day ${day} - ${comment}"
    # Add and commit unstagged changes
    if [ -n "$(git ls-files --other --exclude-standard)" ]; then
        echo "Untracked files found. Do you want to add them ?"
        for f in $(git ls-files --other --exclude-standard); do
            add $f
        done
    fi
    if ! $(git diff --quiet); then
        echo "Unstagged files found."
        for f in $(git diff --name-only); do
            add $f
        done
    fi
    if ! $(git diff --quiet --staged); then
        echo "Will commit staged uncommitted files."
        git commit -m "${comment}" || die "Unable to commit"
    fi
    # Push to remote
    #git push -u origin ${bname}

}

check_branch() {
    exp_branch=$1;shift
    cur_branch=$(git rev-parse --abbrev-ref HEAD)
    [[ ${exp_branch} == ${cur_branch} ]] || die "You must be on ${exp_branch} to execute this action"
}

doit() {
    action=$1;shift
    day=$1;shift
    DAY_FOLDER=${YEAR}/${day}
    case ${action} in
        'begin')
            begin
            ;;
        'save')
            save "$@"
            ;;
        'end')
            end
            ;;
        *)
            echo "Action '${action}' not supported"
            ;;
    esac
}

if [ $# -lt 2 ]; then
    usage
    exit 1
fi

doit "$@"

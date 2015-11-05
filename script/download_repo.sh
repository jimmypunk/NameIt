path="$(pwd)/$1"
echo $path
mkdir -p /tmp/exp_dir
cd /tmp/exp_dir

cat $path| head -n 5 | cut -d',' -f1 | while read line
do
    git clone $line
done
cd - 
# Shell Scripting

Name: Anzar
Enrollment Number: 24BCS10289

These Bash scripts practise file operations, input, variables, functions,
conditions, loops, and system information.

Run the commands from the `Shell-s2` directory:

```bash
cd Shell-s2
```

## 1. Create a folder and file

File: `hello.sh`

```bash
bash hello.sh
```

Commands used:

```bash
mkdir -p test
cd test
echo "This is my logfile" > app.log
echo "Initial content set: $(cat app.log)"
read -r user_input
echo "$user_input" > app.log
cat app.log
```

## 2. Overwrite a file

File: `data.sh`

```bash
bash data.sh
```

Commands used:

```bash
mkdir -p data1
cd data1
echo "This is a log file." > app.log
cat app.log
echo "This is my file" > app.log
cat app.log
```

The `>` operator overwrites the existing file content.

## 3. Append to a file

File: `script1.sh`

```bash
bash script1.sh
```

Commands used:

```bash
mkdir -p test
cd test
echo "This is file1" > app.log
echo "This is file2" >> app.log
cat app.log
```

The `>>` operator appends content without deleting the existing content.

## 4. Take user input

File: `input.sh`

```bash
bash input.sh
```

Commands used:

```bash
read -r -p "Enter your name: " name
read -r -p "Enter your roll number: " roll_number
read -r -p "Enter your comment: " comment

echo "My name is $name"
echo "My roll number is $roll_number"
echo "My comment is: $comment"
```

## 5. Use variables

File: `variable.sh`

```bash
bash variable.sh
```

Commands used:

```bash
name="Anzar"
roll="123"
comment="This class is awesome"

echo -e "Name: $name\nRoll: $roll\nComment: $comment"
```

## 6. Use a function

File: `function.sh`

```bash
bash function.sh
```

Commands used:

```bash
show_info() {
    echo "This is a function"
    echo "This is a function to show information"
}

show_info
```

## 7. Use a `for` loop

File: `loop.sh`

```bash
bash loop.sh
```

Commands used:

```bash
for i in {1..5}
do
    echo "This is iteration number $i"
done
```

## 8. Create a system information report

File: `task.sh`

```bash
bash task.sh
```

Commands used:

```bash
mkdir -p task
cd task
echo "Current Date: $(date)" > task.log
echo "Process: $(ps)" >> task.log
echo "Hostname: $(hostname) and username $(whoami)" >> task.log
echo "Process Info: $(ps)" > process.log
echo "Disk usage: $(df -h)" >> process.log
```

The script writes the current date, process information, hostname, username,
and disk usage to files.

## 9. Use an `if` condition

File: `condition.sh`

```bash
bash condition.sh
```

Commands used:

```bash
read -p "Enter your age: " age

if [ "$age" -lt 0 ]; then
    echo "Invalid age. Please enter a valid age."
elif [ "$age" -lt 13 ]; then
    echo "You are a child."
elif [ "$age" -lt 20 ]; then
    echo "You are a teenager."
else
    echo "You are an adult."
fi
```

## 10. Use a `while` loop with input

File: `while-loop.sh`

```bash
bash while-loop.sh
```

Commands used:

```bash
while true; do
    read -r -p "Enter a number (or 'q' to quit): " input

    if [[ "$input" == "q" ]]; then
        echo "Exiting the loop."
        break
    elif ! [[ "$input" =~ ^[0-9]+$ ]]; then
        echo "Invalid input. Please enter a valid number."
        continue
    fi

    echo "You entered: $input"
done
```

## Summary

This session covers Bash variables, user input, file creation, output
redirection, appending, functions, conditions, and loops. The scripts also
use common system commands such as `date`, `hostname`, `whoami`, `df`, and
`ps`.

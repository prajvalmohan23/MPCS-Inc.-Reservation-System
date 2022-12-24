import sys

def main():
    #save preexisting data elsewhere.
    file = open('tests/backup.txt','w')
    file.close()

    if len(sys.argv) > 1 and sys.argv[1] == "clear":
        return
    with open('data/data.txt','r') as firstfile, open("tests/backup.txt",'a') as secondfile: 
        # read content from first file
        for line in firstfile:  
            # append content to second file
            secondfile.write(line)

    #clear preexisting data file.
    file = open("data/data.txt","w")
    file.close()

    if len(sys.argv) > 1 and sys.argv[1] == "clear":
        return
    with open('tests/testingdata.txt','r') as firstfile, open('data/data.txt','a') as secondfile: 
        # read content from first file
        for line in firstfile:  
            # append content to second file
            secondfile.write(line)

if __name__ == "__main__":
    main()
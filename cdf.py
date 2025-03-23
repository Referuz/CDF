# CDF = Cripted Data Format
# Library to cript files
# @Torres

# Note
## Title
### Code

import os
import time
import colorama
from colorama import Fore
from random import choice
colorama.init()

cyan = Fore.LIGHTCYAN_EX
green = Fore.LIGHTGREEN_EX
yellow = Fore.LIGHTYELLOW_EX
red = Fore.LIGHTRED_EX
blue = Fore.LIGHTBLUE_EX
magenta = Fore.LIGHTMAGENTA_EX
reset = Fore.RESET

def pctrl(title,object): #################### point coltrols to view errors or proccess you wanna see
    print(f"PCTRL_{title}",object)

def rand_key():
    dictionary = """abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!"#$%&/()=¡¿'¨*][;:_,.-<>^°|¬`~"""
    dictionary = list(dictionary)
    pwrd = []
    for i in range(16):
        char = choice(dictionary)
        dictionary.remove(char)
        pwrd.append(char)
    pwrd = ''.join(pwrd)
    return pwrd


def extension(mainKey,extension,action=None):
    out = []
    for i in range(len(extension)):
        out_ = []
        for j in range(len(extension[i])):
            _out_ = []
            for k in range(len(mainKey)):
                if action == "crypt": 
                    xor = ord(extension[i]) ^ mainKey[k]
                    out_.append(xor)
                if action == "decrypt":
                    xor = extension[i][j] ^ mainKey[k]
                    _out_.append(xor)
                if action != "crypt" and action != "decrypt": print("Especifica accion...")
            if action == "decrypt": out_.append(_out_)
        out.append(out_)
    return out

def xor(data,mainKey):
    list0 = []
    for i in range(len(data)):
        xor0 = data[i] ^ mainKey
        list0.append(xor0)
    return list0

def xor_data(data,mainKey):
    out = data
    for i in range(len(mainKey)):
        out_ = xor(out,mainKey[i])
        out = out_
    return out

def heavy_xor(block, key):
    encrypted_block = bytearray()
    for i in range(len(block)):
        encrypted_block.append(block[i] ^ key[i % len(key)])  # XOR cíclico
    return encrypted_block

def heavy_key(key):
    ordKey = [key[i:i+4]for i in range(0,len(key),4)]
    ordKey = [ord(x)for i in ordKey for x in i]

    newKey = [key[8:12],key[0:4],key[12:16],key[4:8]]
    newKey = [ord(x)for i in newKey for x in i]

    keyResult = [ordKey[i] ^ newKey[i] for i in range(len(ordKey))]
    keyResult = [[i,i*2] for i in keyResult]

    return keyResult
    
def heavy_encrypt(key, input_file, output_file,ext=None):
    BLOCK_SIZE = 1024 * 1024 # 1 MB
    key_length = len(key)
    
    if key_length != 32:
        print(f"{red}Something was wrong with your key...{reset}")
        return False
    try:    
        with open(input_file, "rb") as f_in, open(output_file, "wb") as f_out:
            while True:
                block = f_in.read(BLOCK_SIZE)  # Leer un bloque del archivo
                if not block:
                    break  # Fin del archivo
                encrypted_block = heavy_xor(block, key)  # Aplicar XOR al bloque
                f_out.write(encrypted_block)  # Escribir el bloque encriptado
                if __name__ == "__main__": print(f"{yellow}Loading... Solving blocks of uncoded data... [x%]{reset}")
            if ext != None and ext != "": 
                x01 = "\n"+str(ext)
                x01 = x01.encode("utf-8")
                f_out.write(x01)
        os.remove(input_file)
        return True
    except Exception as e:
        print(f"{red}Error during encryption: {e}{reset}")
        return False

def manual_barr(progress):
    if __name__ == "__main__":
        progressN = int((progress/100)*40)
        print(f"{yellow}Loading, solving blocks of uncoded data...{reset}")
        print(f"[{blue}{'='*progressN}{' '*(40-progressN)}]{green}{progress}{'%'}{reset}")
    else: return None

def key_cert(data):
    if len(data) == 16 and " " not in data: # Check the lenght of the key
        return True
    else:
        return False
    
def path_cert(data):
    if os.path.exists(data):
        return True
    else:
        return False

def crypt(key=None,path=None,console=None):
    """ key = password with lenght of 16 chars\n
        path = path of your file, in case you want to cript it\n
        console = consol entry
        >>  Please only use path or console at once, not bouth at same time\n
        It is necesary the key and path or console data
    """

    fileName = None

    if key_cert(key) != False: ##### Keys
        key1 = key[:10] # long. 10
        key1 = [ord(i) for i in key1]

        key2 = key[-6:] # long. 6
        key2 = [ord(i) for i in key2]

        key3 = [key1[3],key2[2],key1[4],key2[3]] # long. 4

        key4 = [key2[0],key2[5]] # long. 2
        
    else:
        print("The leng of the key it has to be 16 chars and whitout blank spaces...")

    if os.path.exists(path): # Check if the file exists
        fileName,fileExtension = os.path.splitext(path) # Get name and extension from the file
        if fileExtension != ".txt":
            fileSize = os.path.getsize(path)
            if fileSize > 3*1014*1024: #3MB
                keyExtend = heavy_key(key)
                keyExtend = [x for i in keyExtend for x in i]
                newFileName = fileName+".cdf"
                cryptedExt = extension(key4, fileExtension, "crypt")
                cryptedExt = [str(i) for i in cryptedExt]
                heavy_encrypt(keyExtend, path, newFileName, cryptedExt)
                return
            else:
                with open(path,"rb")as file:
                    lines = file.read()
                    data = list(lines) # Get decimal data from the file diferent to .txt
        else:
            with open(path,"r")as file:
                lines = file.read()
                data = [ord(i) for i in lines] # Get decimals from .txt file
        if console != None and console != "":
            print("Please just use one of the options. ONLY path, or ONLY console entry")
    else:
        if console != None and console != "":
            data = [ord(i) for i in console] # Get decimal from consol entry
        else:
            print("Please enter path or text to crypt it\n FILE: (\"key\",\"file_path\")\n CONSOLE: (\"key\",None,\"data\")")
    #****************************************
    ## __First_step_of_encryption
    print(f"{yellow}Loading please wait...{reset}")
    manual_barr(0)
    out01 = xor_data(data,key1)
    out02 = xor_data(out01,key2)
    results = xor_data(out02,key3)
    #****************************************
    manual_barr(32)
    #****************************************
    ## __Second_step_of_encryption
    hexaBlocks = [results[i:i+len(key2)] for i in range(0,len(results),len(key2))] # Make blocks acord lenght of second key, those are hexadecimal format
    blocks = []
    for i in hexaBlocks:
        block = []
        for x in i:
            block.append(x)
        blocks.append(block) # Transform the blocks to decimal format
    out = []
    for i in range(len(blocks)):
        criptedBlock = []
        for j in range(len(blocks[i])):
            xor = blocks[i][j] ^ key2[j] # Each data block xor acord position of key's chars
            criptedBlock.append(xor)
        out.append(criptedBlock)
    out = [x for i in out for x in i] # Final result of XOR operation between data and second key
    #******************************************
    manual_barr(64)
    #******************************************
    # __Third_step_of_encryption
    out = [out[i:i+len(key3)] for i in range(0,len(out),len(key3))] # Makes blocks with lenght of third key
    newOut = []
    for i in range(len(out)):
        block = []
        for j in range(len(out[i])):
            times = out[i][j] * key3[j] # Makes a multiplication acording third key position and data blocks
            block.append(times)
        newOut.append(block)
    newOut = [x for i in newOut for x in i] # Final results of the encryption
    #************************************************************
    manual_barr(99)
    time.sleep(2)
    manual_barr(100)
    #************************************************************
    finalOut = []
    for i in range(len(newOut)):
        finalOut.append(hex(newOut[i]))

    if fileName and fileExtension != None:
        cryptedExt = extension(key4,fileExtension,"crypt")
        cryptedExt = [str(i)for i in cryptedExt]
        finalOut = ', '.join(str(i) for i in finalOut)
        newName = fileName+".cdf"
        os.rename(path,newName) # Rename de file as the same name but with .cdf, example.png.cdf
        with open(newName,"w")as file:
            file.write(finalOut) # Send the results of the encriptation to the new renamed file
        with open(newName,"a+")as file:
            file.write("\n"+str(cryptedExt))
    else:
        return finalOut # If fileName and FileExtension does not existe, it is because the user made a consol 
                    # entry, so the output would be in the same function
    #********************************************

def decrypt(key=None,path=None,console=None):
    """ key = password with lenght of 16 chars\n
        path = path of your file, in case you want to cript it\n
        console = consol entry
        >>  Please only use path or console at once, not bouth at same time\n
        It is necesary the key and path or console data
    """
    try:
        dataSize = None
        fileName = None
        if key_cert(key) != False:
            key1 = key[:10] # long. 10
            key1 = [ord(i) for i in key1]

            key2 = key[-6:] # long. 6
            key2 = [ord(i) for i in key2]

            key3 = [key1[3],key2[2],key1[4],key2[3]] # long. 4

            key4 = [key2[0],key2[5]] # long. 2
        else:
            print("The leng of the key it has to be 16 chars and whitout blank spaces...")
            return
        if os.path.exists(path):
            fileName,fileExtension = os.path.splitext(path)
            fileSize = os.path.getsize(path)
            if fileSize > 3*1024*1024: #3MB
                keyExtend = heavy_key(key)
                keyExtend = [x for i in keyExtend for x in i]
                dataSize = "__HEAVY__"
            if fileExtension != ".cdf":
                print(f"{red}The file shud be .cdf and not other extension, like {fileExtension}{reset}")
                if __name__ == "__main__":
                    main()
                else:
                    return None
            # MAKE A VALIDATION WITH THE EXTENSION PART OF THE FILE
            if dataSize != "__HEAVY__":
                with open(path,"r")as file: 
                    lines = file.readlines()
                    newLines = lines[:-1]
                dataExtension = lines[-1].strip()
                dataExtension = dataExtension.replace("'[","")
                dataExtension = dataExtension.replace("]'","")
                dataExtension = dataExtension.strip("[]").split(",")
                dataExtension = [int(i)for i in dataExtension]
            else:
                with open(path,"rb")as file: 
                    lines = file.readlines()
                    newLines = lines[:-1]
                dataExtension = lines[-1]
                dataExtension = dataExtension.decode("utf-8")
                dataExtension = dataExtension.replace("'[","")
                dataExtension = dataExtension.replace("]'","")
                dataExtension = dataExtension.strip("[]").split(",")
                dataExtension = [int(i) for i in dataExtension]
            confirmKey = ""
            
            dataExtension = [dataExtension[i:i+2]for i in range(0,len(dataExtension),2)]

            decryExt = extension(key4,dataExtension,"decrypt")

            finalDataExtension = []
            for i in range(len(decryExt)):
                for j in range(len(decryExt[i])):
                    for _ in range(len(decryExt[i][j])):
                        if decryExt[i][0][0] == decryExt[i][1][1]: confirmKey = "Success"
                        if decryExt[i][0][1] == decryExt[i][1][0]: confirmKey = "Success"
                dataExtensionList = chr(decryExt[i][0][0])
                finalDataExtension.append(dataExtensionList)
            finalDataExtension = ''.join(finalDataExtension)
            if confirmKey == "Success":
                if dataSize != "__HEAVY__":
                    with open(path,"w")as file:
                        file.write(''.join(line.rstrip() + '\n' for line in newLines[:-1]))
                        file.write(newLines[-1].rstrip())
                else:pass
                    #with open(path,"wb")as file:
                        #file.write(b''.join(line.rstrip() + b'\n' for line in newLines[:-1]))
                        #file.write(newLines[-1].rstrip())
            else:
                print(f"{yellow}\nWarning, stopping proces!!, wrong key...\n{reset}")
                time.sleep(2)
                print(f"{red}\nSomething was wrong with your key, try again, WRONG KEY!!!\n{reset}")
                if __name__ == "__main__":
                    main()
                else:
                    return None
                

            if dataSize != "__HEAVY__":
                with open(path,"r")as file:
                    data = file.read()
                    data = data.strip("[]").split(",")
                    data = [int(i,16)for i in data]
                    data = [data[i:i+len(key3)]for i in range(0,len(data),len(key3))]
                    # If path exists it would be opened and read, then cut in blocks with lenght of the third key
                if console != None and console != "":
                    print("Please just use one of the options. ONLY path, or ONLY console entry")
        else:
            if console != None and console != "":
                console = console.replace("[","")
                console = console.replace("]","")
                console = console.replace("'","")
                console = console.strip("[]").split(",")
                console = [int(i,16)for i in console]
                data = [console[i:i+len(key3)] for i in range(0,len(console),len(key3))]

                # It means that the user did not use path, so it cuts the console entry with lenght of third key
            else:
                print("Please enter path or text to crypt it\n FILE: (\"key\",\"file_path\")\n CONSOLE: (\"key\",None,\"data\")")
        #***************************************************
        if dataSize != "__HEAVY__":
            manual_barr(5)
            # __First_step_of_decription
            ress = []
            for i in range(len(data)):
                block = []
                for j in range(len(data[i])):
                    div = data[i][j] / key3[j] # Makes a division between each position of the data's blocks and third key's blocks
                    block.append(int(div))
                ress.append(block)
            ress = [x for i in ress for x in i]
            ress = [ress[i:i+len(key2)] for i in range(0,len(ress),len(key2))] # Final result cuted in blocks with lenght of second key
            # **************************************************
            manual_barr(32)
            #***************************************************
            #__Second_step_of_decryption
            out = []
            for i in range(len(ress)):
                salidas = []
                for j in range(len(ress[i])):
                    xor = ress[i][j] ^ key2[j] # Reverts XOR between each position of bouth blocks, data and second key
                    salidas.append(xor)
                out.append(salidas)
            out = [x for i in out for x in i] # Final list of XOR
            #***************************************************
            manual_barr(64)
            #***************************************************
            #__Last_step_of_decryption
            in01 = xor_data(out,key3)
            in02 = xor_data(in01,key2)
            res = xor_data(in02,key1)

            if fileName != None:
                finalOut = bytes(res)
                newName = fileName+finalDataExtension
                os.rename(path,newName) # Rewrite the name as original one, example.png
                with open(newName,"wb")as file:
                    file.write(finalOut) # Rewrite the content of the .cdf to decrypted format
            else:
                finalOut = [chr(i) for i in res] # Makes the data to riginal one "chars"
                finalOut = ''.join(finalOut) 
                return finalOut # Returns data, because the user made a consol entry
            manual_barr(99)
            time.sleep(2)
            manual_barr(100)
        # *************************************************
        else: 
            newName = fileName+finalDataExtension
            heavy_encrypt(keyExtend,path,newName)
    except UnicodeDecodeError:
        print(f"{red}Error: It couldn't decode the file. Check the correct encryption of the file.{reset}")
    except Exception as e:
        print(f"{red}Error diring decryption: {e}{reset}")


def info():
    dat = f"""
{blue}##############      MAIN FUNCTIONS      ##############{reset}
{blue}#{magenta}####   ----------   Library mode   ----------   ####{blue}#
{blue}#{green}#  FILES                                            {blue}*
{blue}#{yellow} crypt("Drft523x()jK@dZ0", "prueba01.png")          {blue}*
{blue}#{red}        password,            file_path              {blue}*
{blue}#{yellow} decrypt("Drft523x()jK@dZ0","prueba01.cdf")         {blue}*
{blue}#{red}        password,            cripted_file_path      {blue}*
{blue}******************************************************
{blue}#{green}#  CONSOL                                           {blue}*
{blue}#{yellow} crypt("Drft523x()jK@dZ0", "", "h2")                {blue}*
{blue}#{red}         password,        blank,  data              {blue}*
{blue}#{yellow} decrypt("Drft523x()jK@dZ0","",['0x2bf4', '0x680']) {blue}*
{blue}#{red}         password,        blank,  cripted_data      {blue}*
{blue}******************************************************{reset}
"""
    print(dat)


def main():
    title = f'''\n{cyan} 
            ..gg88"""""bbggddd ``77MMMM"""""YYbb..    ``77MMMM""""""YYMMMM
         ..ddPP''         ``MM     MMMM       ``Ybb..    MMMM         ``MM
        /dMM''              ``     MMMM         ``Mbb    MMMM            Y
        MMMM                       MMMM           MMMM   MMMM     d
        MMMM  {magenta}Made by Juan Diego{cyan}   MMMM   {magenta}Torres{cyan}  'MMM   MMMM"""MMM   {magenta}Infante{cyan}
        7MMM:                      MMMM           MMMM   MMMM     Y
         MMMM:.                    MMMM         ,,MPP    MMMM      
          `Mbbb..         ,''      MMMM       ,,dPP''    MMMM
            ``""bbmmmmmdd''    ..JJMMMMmmmmmddPP''    ..JJMMMMLL..{reset}'''
    print(title)

    while True:
        print(f"\n{green}Welcome to CDF, choose your option...{reset}")
        print(f"""\n  {yellow}1.- {blue}Crypt any file (Heavy files take time){reset}
  {yellow}2.- {magenta}Crypt by console
  {yellow}3.- {blue}Decrypt any file (Heavy files take time)
  {yellow}4.- {magenta}Decrypt by console
  {yellow}5.- {cyan}Get a random 16 chars password
  {red}6.- Exit{reset}""")
        option = input(f"{cyan}\n~| {reset}")
        if option == "1":
            print(f"Press {red}[Q]{reset} to exit\nPress {green}[B]{reset} to {blue}main menu{reset}")

            action = f"{green}crypt{red}~{blue}file{yellow}|{reset}"

            mainKey = input(f"{yellow}Write your key, remember only 16 chars and no blank spaces...\n{blue}{action}{cyan}~| {reset}")
            if mainKey.lower() == "q": quit()
            if mainKey.lower() == "b": continue

            if key_cert(mainKey) == False:
                print(f"{red}The leng of the key it has to be 16 chars and whitout blank spaces...{reset}")
                continue

            mainPath = input(f"{yellow}Write the file path...\n{blue}{action}{cyan}~| {reset}")
            if mainPath.lower() == "q": quit()
            if mainPath.lower() == "b": continue

            if path_cert(mainPath) == False:
                print(f"{red}Please write a correct file path...{reset}")
                continue

            crypt(mainKey,mainPath)
            print(f"\n{cyan}Success!!!{reset}")
            continue
        elif option == "2":
            print(f"Press {red}[Q]{reset} to exit\nPress {green}[B]{reset} to {blue}main menu{reset}")

            action = f"{green}crypt{red}~{blue}console{yellow}|{reset}"

            mainKey = input(f"{yellow}Write your key, remember only 16 chars and no blank spaces...\n{blue}{action}{cyan}~| {reset}")
            if mainKey.lower() == "q": quit()
            if mainKey.lower() == "b": continue

            if key_cert(mainKey) == False:
                print(f"{red}The leng of the key it has to be 16 chars and whitout blank spaces...{reset}")
                continue           

            data = input(f"{yellow}Write your data...\n{blue}{action}{cyan}~| {reset}")
            if data.lower() == "q": quit()
            if data.lower() == "b": continue

            print(f"{blue}OUT: {reset}",crypt(mainKey,"",data))
            print(f"\n{cyan}Success!!!{reset}")
            continue
        elif option == "3":
            print(f"Press {red}[Q]{reset} to exit\nPress {green}[B]{reset} to {blue}main menu{reset}")

            action = f"{green}decrypt{red}~{blue}file{yellow}|{reset}"
            
            mainKey = input(f"{yellow}Write your key, remember only 16 chars and no blank spaces...\n{blue}{action}{red}~| {reset}")
            if mainKey.lower() == "q": quit()
            if mainKey.lower() == "b": continue

            if key_cert(mainKey) == False:
                print(f"{red}The leng of the key it has to be 16 chars and whitout blank spaces...{reset}")
                continue            

            mainPath = input(f"{yellow}Write the file path...\n{blue}{action}{red}~| {reset}")
            if mainPath.lower() == "q": quit()
            if mainPath.lower() == "b": continue

            if path_cert(mainPath) == False:
                print(f"{red}Please write a correct file path...{reset}")
                continue

            decrypt(mainKey,mainPath)

            print(f"\n{cyan}Success!!!{reset}")
            continue
        elif option == "4":
            print(f"Press {red}[Q]{reset} to exit\nPress {green}[B]{reset} to {blue}main menu{reset}")

            action = f"{green}decrypt{red}~{blue}console{yellow}|{reset}"
            
            mainKey = input(f"{yellow}Write your key, remember only 16 chars and no blank spaces...\n{blue}{action}{cyan}~| {reset}")
            if mainKey.lower() == "q": quit()
            if mainKey.lower() == "b": continue

            if key_cert(mainKey) == False:
                print(f"{red}The leng of the key it has to be 16 chars and whitout blank spaces...{reset}")
                continue

            data = input(f"{yellow}Write your data...\n{blue}{action}{cyan}~| {reset}")
            if data.lower() == "q": quit()
            if data.lower() == "b": continue

            print(f"{blue}OUT: {reset}",decrypt(mainKey,"",data))
            print(f"\n{cyan}Success!!!{reset}")
            continue
        elif option == "5":
            print(f"{magenta}Here you have your 16 chars password: {cyan} {rand_key()}{reset}")
            continue
        elif option == "6":
            exit()
        elif option.lower() == "info()":
            print(f"{yellow}Here you have more options of uses as a library...{reset}")
            print(f"{yellow}If this version is a .exe version, please use .py to use as a library{reset}")
            info()
        else:
            print(f"{red}Wrong option, please check your entry...\n{reset}")

if __name__ == "__main__":
    main()
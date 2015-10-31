__author__ = 'titan'
import sha3
import hashlib
import bitstring

DATASIZE = 8

sampleText = """The Letter

It was November. Although it was not yet late, the sky was dark when I turned into Laundress Passage. Father had finished for the day, switched off the shop lights and closed the shutters; but so I would not come home to darkness he had left on the light over the stairs to the flat. Through the glass in the door it cast a foolscap rectangle of paleness onto the wet pavement, and it was while I was standing in that rectangle, about to turn my key in the door, that I first saw the letter. Another white rectangle, it was on the fifth step from the bottom, where I couldn't miss it.

I closed the door and put the shop key in its usual place behind Bailey's Advanced Principles of Geometry. Poor Bailey. No one has wanted his fat gray book for thirty years. Sometimes I wonder what he makes of his role as guardian of the bookshop keys. I don't suppose it's the destiny he had in mind for the masterwork that he spent two decades writing.

A letter. For me. That was something of an event. The crisp-cornered envelope, puffed up with its thickly folded contents, was addressed in a hand that must have given the postman a certain amount of trouble. Although the style of the writing was old-fashioned, with its heavily embellished capitals and curly flourishes, my first impression was that it had been written by a child. The letters seemed untrained. Their uneven strokes either faded into nothing or were heavily etched into the paper. There was no sense of flow in the letters that spelled out my name. Each had been undertaken separately -- M A R G A R E T L E A -- as a new and daunting enterprise. But I knew no children. That is when I thought, It is the hand of an invalid.

It gave me a queer feeling. Yesterday or the day before, while I had been going about my business, quietly and in private, some unknown person -- some stranger -- had gone to the trouble of marking my name onto this envelope. Who was it who had had his mind's eye on me while I hadn't suspected a thing?

Still in my coat and hat, I sank onto the stair to read the letter. (I never read without making sure I am in a secure position. I have been like this ever since the age of seven when, sitting on a high wall and reading The Water Babies, I was so seduced by the descriptions of underwater life that I unconsciously relaxed my muscles. Instead of being held buoyant by the water that so vividly surrounded me in my mind, I plummeted to the ground and knocked myself out. I can still feel the scar under my fringe now. Reading can be dangerous.)

I opened the letter and pulled out a sheaf of half a dozen pages, all written in the same laborious script. Thanks to my work, I am experienced in the reading of difficult manuscripts. There is no great secret to it. Patience and practice are all that is required. That and the willingness to cultivate an inner eye. When you read a manuscript that has been damaged by water, fire, light or just the passing of the years, your eye needs to study not just the shape of the letters but other marks of production. The speed of the pen. The pressure of the hand on the page. Breaks and releases in the flow. You must relax. Think of nothing. Until you wake into a dream where you are at once a pen flying over vellum and the vellum itself with the touch of ink tickling your surface. Then you can read it. The intention of the writer, his thoughts, his hesitations, his longings and his meaning. You can read as clearly as if you were the very candlelight illuminating the page as the pen speeds over it.

Not that this letter was anything like as challenging as some. It began with a curt "Miss Lea"; thereafter the hieroglyphs resolved themselves quickly into characters, then words, then sentences.

This is what I read:"""

def keystream(seedHandle,size):
    s = hashlib.sha3_512()
    seed = 0
    previousHash = ''
    try:
        byte = seedHandle.read(65536)
        while byte != "":
            s.update(byte)
            byte = seedHandle.read(65536)
    finally:
        previousHash = hash = s.hexdigest()
        seed = bitstring.BitArray(hex=hash).bin

    while len(seed) < size:
        s = hashlib.sha3_512()
        s.update(previousHash)
        previousHash = hash = s.hexdigest()
        seed = str(seed) + str(bitstring.BitArray(hex=hash).bin)
    return bitstring.BitArray(bin=seed).bin[0:size]


#keystream = seed[0:len(stringToEncrypt.bin)]
def convertToByteArray(bitString):
    return [bitString[i:i+DATASIZE] for i in range(0, len(bitString), DATASIZE)]

def convertBinaryToAscii(string):
    tempString = ""
    for byte in convertToByteArray(string):
        tempString += chr(int(byte,2))
    return tempString
def decrypt(seed,cyphertext):
    key = keystream(seed,len(cyphertext))
    tempKey = convertToByteArray(key)

    cyphertext = convertToByteArray(cyphertext)
    decryptedMessage = ''
    for bytePos in range(0,len(cyphertext)):
        decryptedMessage += '{:08b}'.format((int(cyphertext[bytePos],2)^int(tempKey[bytePos],2)))

    decryptedMessage = bitstring.BitArray(bin=decryptedMessage).bin
    return decryptedMessage


def encrypt(seed,message):
    stringToEncrypt = ''
    for elem in message:
        stringToEncrypt += str(elem.encode("hex"))
    stringToEncrypt = bitstring.BitArray(hex=stringToEncrypt)

    key = keystream(seed,len(stringToEncrypt.bin))

    tempKey = convertToByteArray(key)
    tempMessage = convertToByteArray(stringToEncrypt.bin)

    cyphertext = ''
    for bytePos in range(0,len(tempMessage)):
        cyphertext += '{:08b}'.format((int(tempMessage[bytePos],2)^int(tempKey[bytePos],2)))

    cyphertext = bitstring.BitArray(bin=cyphertext).bin
    return cyphertext

handle = open("seed.jpg","rb")
en = encrypt(handle,sampleText)
print convertBinaryToAscii(en)
handle.close()

handle = open("seed.jpg","rb")
test = str(decrypt(handle,en))
print convertBinaryToAscii(test)




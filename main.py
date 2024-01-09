import openai
from pypdf import PdfReader # most basic PDF text extractor
# more adnvanced alternatives to deal with figures, images, tables, equations
# etc. would be PDFMiner and Pytesseract
import PDFtoMD as PDFtoMD
import csv
from api_keys import OpenAI_KEY

# Load your API key from an environment variable or secret management service
openai.api_key = OpenAI_KEY

# READ PDF & GET AN EARLY ESTIMATE
# ================================
def firstRead(PDF_TITLE):
    reader = PdfReader(PDF_TITLE)
    number_of_pages = len(reader.pages)
    text = ""
    for page in range(number_of_pages):
        text += str(reader.pages[page].extract_text())
    print("=========================================")
    print("PDF TITLE:", PDF_TITLE)
    print("PAGES:", number_of_pages)
    print("TEXT LENGTH:", len(text), "CHARACTERS")
    print("WORDS:", len(text.split()))
    print("ESTIMATED CARDS:", round(len(text.split())/200))
    print("ESTIMATED PRICE:", round(len(text.split())/200*0.04,2), "€")

# HELPER FUNCTIONS
# ================================
def read_file(file_path):
    # Reads the contents of a file.
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()

def chunkify(content, chunk_size):
    # Splits content into chunks of size chunk_size.
    words = content.split()
    for i in range(0, len(words), chunk_size):
        yield ' '.join(words[i:i + chunk_size])


# CREATE QUESTIONS & ANSWERS USING A LLM
# ======================================
def genQuestions(file_path, chunk_size):
    # MAIN LOOP
    # read md file into string
    content = read_file(file_path)

    # chunk the string into smaller parts
    chunks = list(chunkify(content, chunk_size))
    responses = []

    # execute the loop for each chunk
    # "Du bist ein Lernkartengenerator. Alle Symbole und Kontext werden innerhalb der Frage und Antwort erklärt. Gleichungen werden in LaTex formatiert mit \( \) und \[ \]. Sie sprechen die Sprache des gegebenen Textes. Sie erhalten einen Text und müssen auf der Grundlage des Textes Fragen und Antworten mit den Präfixen Q: und A: generieren. Beende Q und A mit \n. Sie beziehen so viele Informationen wie möglich aus dem Text ein. Ausführliche Antworten! Sie werden keinen Absatz verpassen. Der Text ist:"
    for index, chunk in enumerate(chunks, 1):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",   # gpt-3.5-turbo
                temperature=1,
                messages=[
                    {"role": "system", 
                    "content": "You are a flashcard generator. All symbols and context are explained within the question and answer. Equations are formatted in LaTex with \( \) and \[ \]. They speak the language of the given text. You are given a text and based on the text you have to generate questions and answers with the prefixes Q: and A:. End Q and A with \n. You include as much information as possible from the text. Detailed answers! You won't miss a paragraph. The text is:"},
                    {"role": "user", "content": chunk}]
                )
            responses.append([response['choices'][0]['message']['content']])
            print("=========================================")
            print(f"Chunk {index}:\n{chunk}\n{'-'*40}")
            print(f"FLASHCARDS:\n{response['choices'][0]['message']['content']}")

            # Save all the raw responses to a .txt file
            with open("responses.txt", "w", encoding='utf-8') as file:
                writer = csv.writer(file)
                for response in responses:
                    writer.writerow(response)  # write data
            
        except:
            print("Error in generating questions and answers")
            print("Chunk:", chunk)
            print("=========================================")
            pass
    
# FORMAT THE DECK
# ================================
def formatDeck(file_path):
    responses = []
    with open(file_path, "r", encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            responses.append(row)
    responses = [item for item in responses if item != []]

    print(responses)
    print(len(responses))
    # collecting all the questions and answers from the .txt file
    # and reformatting them to be used by Anki
    print("...collecting QandAs...")
    questions = []
    answers = []
    for response in responses:
        # Split the text by 'Q:'
        cards = [s.strip() for s in response[0].split('Q:') if s]
        # Create a list of questions and answers
        for card in cards:
            try:
                q, a = card.split('A:')
                questions.append(q.strip())
                answers.append(a.strip())
            except:
                print("Error in splitting Q and A")
                print(card)
                print("=========================================")
                pass

    # Write the final .txt file to be used by Anki!
    with open("QandAs.txt", "w", encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        for i in range(len(questions)):
            writer.writerow([questions[i], answers[i]])

# INPUT PARAMETERS
# ================================
PDF_TITLE = "this_is_your_pdf.pdf"
CHUNK_SIZE = 1000
# ================================

# READ THE PDF AND GET AN EARLY ESTIMATE
firstRead(PDF_TITLE)

# SEND THE PDF FOR MD CONVERSION TO MATHPIX
PDFtoMD.convert(PDF_TITLE)

# READ THE MD FILE AND CREATE THE QUESTIONS & ANSWERS
genQuestions("PDFasMD.md", CHUNK_SIZE)

# FORMAT THE DECK FOR ANKI
formatDeck("responses.txt")
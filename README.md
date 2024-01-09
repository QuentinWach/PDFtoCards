![PDFtoCards](header_image.jpg)

**Take any book or article in PDF form and convert it to a deck of flashcards!**

* 👀 **Recognizes** text, equations, images, and (some) handwriting.
* 🧠 **Understands** the content and context of the PDF.
* ✍🏻 **Summarizes** the PDF as questions and answers systematically.
* 📕 **Reformats** everything into .txt, ready to be used in quiz programs like Anki!

ChatGPT is used for understanding the content and MathPix to extract equations and images.

### ❓ How to use...
1. After installing these scripts as well as the depencies listed below and getting the required API keys, add these in the ``api_keys.py`` file.
2. Put the PDF you want to extract flashcards from into this directory, open the ``main.py`` file and change the ``PDF_TITLE = "this_is_your_pdf.pdf"`` variable to the name of the PDF.
3. Run the script!

### 📂 Dependencies
You will need to install the following two libraries ``openai``, ``pypdf``, and get API keys for ``ChatGPT``  and ``MathPix``. Beware that using both will cost money. Even large textbooks will only cost a few cent though and the decks will be done in minutes not weeks!

---
This is the hacky bare bone version of the software I had written last year trying to add a bunch more features and creating a web app. But I am not a web developer and so eventually lost interest when OpenAI kept releasing more and more cool stuff that made this seem not all that special. I learned a lot about web dev though and if this little thing helped and you like it, come to tell me on [X (formerly Twitter) @quentinwach](https://twitter.com/QuentinWach) 👋🏻.

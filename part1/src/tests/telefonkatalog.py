import mysql.connector  # Using the MySQL connector for Python

# Connect to MariaDB
conn = mysql.connector.connect(
    host="192.168.1.22",  # Replace with your actual MariaDB host
    user="admin",       # Replace with your MariaDB username
    password="Blindbat11!", # Replace with your MariaDB password
    database="telefonkatalog "  # Replace with the name of your MariaDB database
)

cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS personer (
                fornavn VARCHAR(255),
                etternavn VARCHAR(255),
                telefonnummer VARCHAR(20)
            )''')

conn.commit()

def visAllePersoner():
    cursor.execute("SELECT * FROM personer")
    resultater = cursor.fetchall()
    if not resultater:
        print("Det er ingen registrerte personer i katalogen")
        input("Trykk en tast for å gå tilbake til menyen")
        printMeny()
    else:
        print("*****************************************"
              "*****************************************")
        for personer in resultater:
            print("* Fornavn: {:15s} Etternavn: {:15s} Telfonnummer:{:8s}"
                  .format(personer[0], personer[1], personer[2]))
        print("*****************************************"
              "*****************************************")
        input("Trykk en tast for å gå tilbake til menyen")
        printMeny()

# Function to add a new person to the database
def legg_til_person_i_db(fornavn, etternavn, telefonnummer):
    cursor.execute("INSERT INTO personer (fornavn, etternavn, telefonnummer) VALUES (%s, %s, %s)",
              (fornavn, etternavn, telefonnummer))
    conn.commit()

# Function to delete a person from the database
def slett_person_fra_db(fornavn, etternavn, telefonnummer):
    cursor.execute("DELETE FROM personer WHERE fornavn=%s AND etternavn=%s AND telefonnummer=%s",
              (fornavn, etternavn, telefonnummer))
    conn.commit()

def printMeny():
    print("------------------- Telefonkatalog -------------------")
    print("| 1. Legg til ny person                              |")
    print("| 2. Søk opp person eller telefonnummer              |")
    print("| 3. Vis alle personer                               |")
    print("| 4. Avslutt                                         |")
    print("------------------------------------------------------")
    menyvalg = input("Skriv inn tall for å velge fra menyen: ")
    utfoerMenyvalg(menyvalg)

def utfoerMenyvalg(valgtTall):
    if valgtTall == "1":
        registrerPerson()
    elif valgtTall == "2":
        sokPerson()
        printMeny()
    elif valgtTall == "3":
        visAllePersoner()
    elif valgtTall == "4":
        bekreftelse = input("Er du sikker på at du vil avslutte? J/N ")
        if (bekreftelse == "J" or bekreftelse == "j"):
            conn.close()
            exit()
    else:
        nyttForsoek = input("Ugyldig valg. Velg et tall mellom 1-4: ")
        utfoerMenyvalg(nyttForsoek)

def registrerPerson():
    fornavn = input("Skriv inn fornavn: ")
    etternavn = input("Skriv inn etternavn: ")
    telefonnummer = input("Skriv inn telefonnummer: ")

    legg_til_person_i_db(fornavn, etternavn, telefonnummer) # Legger til informasjonen fra input-feltene i databasen som en ny rad

    print("{0} {1} er registrert med telefonnummer {2}"
          .format(fornavn, etternavn, telefonnummer))
    input("Trykk en tast for å gå tilbake til menyen")
    printMeny()

def sokPerson():
    print("1. Søk på fornavn")
    print("2. Søk på etternavn")
    print("3. Søk på telefonnummer")
    print("4. Tilbake til hovedmeny")
    sokefelt = input("Velg ønsket søk 1-3, eller 4 for å gå tilbake: ")
    if sokefelt == "1":
        navn = input("Fornavn: ")
        finnPerson("fornavn", navn)
    elif sokefelt == "2":
        navn = input("Etternavn: ")
        finnPerson("etternavn", navn)
    elif sokefelt == "3":
        tlfnummer = input("Telefonnummer: ")
        finnPerson("telefonnummer", tlfnummer)
    elif sokefelt == "4":
        printMeny()
    else:
        print("Ugyldig valg. Velg et tall mellom 1-4: ")
        sokPerson()

# Function to find a person based on the selected search type (fornavn, etternavn, telefonnummer)
def finnPerson(typeSok, sokeTekst):
    if typeSok == "fornavn":
        cursor.execute("SELECT * FROM personer WHERE fornavn=%s", (sokeTekst,))
    elif typeSok == "etternavn":
        cursor.execute("SELECT * FROM personer WHERE etternavn=%s", (sokeTekst,))
    elif typeSok == "telefonnummer":
        cursor.execute("SELECT * FROM personer WHERE telefonnummer=%s", (sokeTekst,))

    resultater = cursor.fetchall()

    if not resultater:
        print("Finner ingen personer")
    else:
        for personer in resultater:
            print("{0} {1} har telefonnummer {2}"
                  .format(personer[0], personer[1], personer[2]))

printMeny()  # Start the program by displaying the menu

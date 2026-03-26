"""
add_indian_movies.py
Appends a curated set of Indian movies (Hindi/Bollywood, Marathi, Telugu/Tollywood, Tamil/Kollywood)
to movie_dataset.csv in the same format.

Run once: python3 add_indian_movies.py
"""
import csv
import os
import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH   = os.path.join(SCRIPT_DIR, "movie_dataset.csv")
BACKUP     = CSV_PATH + ".bak"

# ── Indian movie data ────────────────────────────────────────────────────────
# Fields: index, budget, genres, homepage, id, keywords, original_language,
#         original_title, overview, popularity, production_companies,
#         production_countries, release_date, revenue, runtime, spoken_languages,
#         status, tagline, title, vote_average, vote_count, cast, crew, director

INDIAN_MOVIES = [
    # ── BOLLYWOOD / HINDI ───────────────────────────────────────────────────
    {
        "title": "3 Idiots", "original_title": "3 Idiots", "original_language": "hi",
        "genres": "Comedy Drama", "keywords": "college friendship engineering india satire",
        "overview": "Two friends search for a third college friend while recounting the hilarious and inspiring events of their university days.",
        "director": "Rajkumar Hirani",
        "cast": "Aamir Khan Madhavan Sharman Joshi Kareena Kapoor Boman Irani",
        "release_date": "2009-12-25", "vote_average": "8.4", "vote_count": "3800",
        "budget": "550000000", "revenue": "2020000000", "runtime": "170", "id": "900001",
        "popularity": "45.2", "tagline": "Pursue Excellence", "status": "Released",
    },
    {
        "title": "Dangal", "original_title": "Dangal", "original_language": "hi",
        "genres": "Biography Drama Sport", "keywords": "wrestling women empowerment father daughters india sports",
        "overview": "Former wrestler Mahavir Singh Phogat trains his daughters to become world-class wrestlers in defiance of tradition.",
        "director": "Nitesh Tiwari",
        "cast": "Aamir Khan Fatima Sana Shaikh Sanya Malhotra Sakshi Tanwar",
        "release_date": "2016-12-23", "vote_average": "8.4", "vote_count": "4200",
        "budget": "700000000", "revenue": "9421900000", "runtime": "161", "id": "900002",
        "popularity": "52.1", "tagline": "", "status": "Released",
    },
    {
        "title": "PK", "original_title": "PK", "original_language": "hi",
        "genres": "Comedy Drama Science Fiction", "keywords": "alien religion india comedy satire",
        "overview": "An alien on Earth loses the remote control that he needs to contact his spaceship. His innocent questions about human religious customs trigger controversy.",
        "director": "Rajkumar Hirani",
        "cast": "Aamir Khan Anushka Sharma Sushant Singh Rajput Boman Irani",
        "release_date": "2014-12-19", "vote_average": "8.1", "vote_count": "3100",
        "budget": "850000000", "revenue": "8540000000", "runtime": "153", "id": "900003",
        "popularity": "41.7", "tagline": "Questions every answer", "status": "Released",
    },
    {
        "title": "Lagaan", "original_title": "Lagaan", "original_language": "hi",
        "genres": "Drama History Sport", "keywords": "cricket colonial india british tax village rebellion",
        "overview": "In 1893 India, a small village decides to challenge their British rulers to a cricket match to avoid paying a harsh land tax.",
        "director": "Ashutosh Gowariker",
        "cast": "Aamir Khan Gracy Singh Rachel Shelley Paul Blackthorne",
        "release_date": "2001-06-15", "vote_average": "8.1", "vote_count": "2800",
        "budget": "250000000", "revenue": "1350000000", "runtime": "224", "id": "900004",
        "popularity": "32.5", "tagline": "Once upon a time in India", "status": "Released",
    },
    {
        "title": "Dil Chahta Hai", "original_title": "Dil Chahta Hai", "original_language": "hi",
        "genres": "Comedy Drama Romance", "keywords": "friendship youth love coming of age road trip",
        "overview": "Three inseparable friends have different perspectives on love — their bond is tested when each faces his own romantic journey.",
        "director": "Farhan Akhtar",
        "cast": "Aamir Khan Saif Ali Khan Akshaye Khanna Preity Zinta Sonali Kulkarni",
        "release_date": "2001-08-10", "vote_average": "7.9", "vote_count": "1900",
        "budget": "150000000", "revenue": "600000000", "runtime": "183", "id": "900005",
        "popularity": "28.4", "tagline": "", "status": "Released",
    },
    {
        "title": "Zindagi Na Milegi Dobara", "original_title": "Zindagi Na Milegi Dobara", "original_language": "hi",
        "genres": "Adventure Comedy Drama Romance", "keywords": "spain road trip friendship bucket list adventure",
        "overview": "Three friends set out on a road trip across Spain completing each other's bucket list challenges before one of them gets married.",
        "director": "Zoya Akhtar",
        "cast": "Hrithik Roshan Farhan Akhtar Abhay Deol Katrina Kaif Kalki Koechlin",
        "release_date": "2011-07-15", "vote_average": "8.2", "vote_count": "2600",
        "budget": "650000000", "revenue": "1530000000", "runtime": "153", "id": "900006",
        "popularity": "35.9", "tagline": "You only live once", "status": "Released",
    },
    {
        "title": "Gangs of Wasseypur", "original_title": "Gangs of Wasseypur", "original_language": "hi",
        "genres": "Action Crime Drama Thriller", "keywords": "coal mafia revenge revenge family feud india gangster",
        "overview": "A coal mafia rivalry spanning several decades triggers a bloody war between three powerful families in Jharkhand.",
        "director": "Anurag Kashyap",
        "cast": "Manoj Bajpayee Nawazuddin Siddiqui Richa Chadha Huma Qureshi",
        "release_date": "2012-06-22", "vote_average": "8.2", "vote_count": "2100",
        "budget": "160000000", "revenue": "600000000", "runtime": "321", "id": "900007",
        "popularity": "33.2", "tagline": "", "status": "Released",
    },
    {
        "title": "Andhadhun", "original_title": "Andhadhun", "original_language": "hi",
        "genres": "Crime Mystery Thriller", "keywords": "blind pianist murder suspense dark comedy",
        "overview": "A series of unexpected events turn a seemingly blind pianist's life upside down after he witnesses a murder.",
        "director": "Sriram Raghavan",
        "cast": "Ayushmann Khurrana Tabu Radhika Apte Anil Dhawan",
        "release_date": "2018-10-05", "vote_average": "8.2", "vote_count": "2900",
        "budget": "120000000", "revenue": "650000000", "runtime": "139", "id": "900008",
        "popularity": "38.6", "tagline": "", "status": "Released",
    },
    {
        "title": "Taare Zameen Par", "original_title": "Taare Zameen Par", "original_language": "hi",
        "genres": "Drama Family", "keywords": "dyslexia child education teacher art school",
        "overview": "An eight-year-old child considered a problem at school is helped by an art teacher who recognises his dyslexia.",
        "director": "Aamir Khan",
        "cast": "Darsheel Safary Aamir Khan Tisca Chopra Vipin Sharma",
        "release_date": "2007-12-21", "vote_average": "8.4", "vote_count": "3400",
        "budget": "250000000", "revenue": "1030000000", "runtime": "165", "id": "900009",
        "popularity": "36.5", "tagline": "Every child is special", "status": "Released",
    },
    {
        "title": "Mughal-E-Azam", "original_title": "Mughal-E-Azam", "original_language": "hi",
        "genres": "Drama History Romance", "keywords": "mughal empire akbar salim anarkali forbidden love classic",
        "overview": "The Mughal Emperor Akbar imprisons Prince Salim to prevent his love affair with a court dancer named Anarkali.",
        "director": "K. Asif",
        "cast": "Dilip Kumar Madhubala Prithviraj Kapoor Durga Khote",
        "release_date": "1960-08-05", "vote_average": "8.1", "vote_count": "1100",
        "budget": "15000000", "revenue": "110000000", "runtime": "197", "id": "900010",
        "popularity": "22.1", "tagline": "", "status": "Released",
    },
    {
        "title": "Deewar", "original_title": "Deewar", "original_language": "hi",
        "genres": "Action Crime Drama", "keywords": "brothers cop smuggler mother india gangster classic",
        "overview": "Two brothers, sons of a disgraced union leader — one becomes a cop, the other a powerful smuggler.",
        "director": "Yash Chopra",
        "cast": "Amitabh Bachchan Shashi Kapoor Nirupa Roy Neetu Singh Parveen Babi",
        "release_date": "1975-01-24", "vote_average": "8.0", "vote_count": "900",
        "budget": "4000000", "revenue": "60000000", "runtime": "174", "id": "900011",
        "popularity": "20.4", "tagline": "", "status": "Released",
    },
    {
        "title": "Sholay", "original_title": "Sholay", "original_language": "hi",
        "genres": "Action Adventure Drama", "keywords": "dacoit revenge village classic bollywood iconic",
        "overview": "Two criminals are hired by a retired police officer to capture a deadly bandit who terrorises a village.",
        "director": "Ramesh Sippy",
        "cast": "Amitabh Bachchan Dharmendra Hema Malini Jaya Bachchan Amjad Khan",
        "release_date": "1975-08-15", "vote_average": "8.2", "vote_count": "1700",
        "budget": "30000000", "revenue": "2500000000", "runtime": "204", "id": "900012",
        "popularity": "30.2", "tagline": "", "status": "Released",
    },
    {
        "title": "Dilwale Dulhania Le Jayenge", "original_title": "Dilwale Dulhania Le Jayenge", "original_language": "hi",
        "genres": "Drama Romance", "keywords": "london punjab nri romance family tradition classic",
        "overview": "A young NRI man and a traditional Punjabi girl fall in love during a Euro trip and must fight for their union.",
        "director": "Aditya Chopra",
        "cast": "Shah Rukh Khan Kajol Amrish Puri Farida Jalal",
        "release_date": "1995-10-20", "vote_average": "8.1", "vote_count": "3200",
        "budget": "40000000", "revenue": "2000000000", "runtime": "189", "id": "900013",
        "popularity": "38.7", "tagline": "Come, fall in love", "status": "Released",
    },
    {
        "title": "Swades", "original_title": "Swades", "original_language": "hi",
        "genres": "Drama", "keywords": "nasa scientist india village development patriotism",
        "overview": "A successful NASA scientist returns to India to bring his childhood nanny to America but finds himself reconnecting with his roots.",
        "director": "Ashutosh Gowariker",
        "cast": "Shah Rukh Khan Gayatri Joshi Kishori Balal",
        "release_date": "2004-12-17", "vote_average": "8.0", "vote_count": "2100",
        "budget": "250000000", "revenue": "480000000", "runtime": "189", "id": "900014",
        "popularity": "28.9", "tagline": "We the people", "status": "Released",
    },
    {
        "title": "Tumbbad", "original_title": "Tumbbad", "original_language": "hi",
        "genres": "Fantasy Horror Mystery Thriller", "keywords": "greed curse goddess gold india supernatural folklore",
        "overview": "A mythological story about a goddess who holds a demon she loves inside her womb — and a man obsessed with her buried gold.",
        "director": "Rahi Anil Barve",
        "cast": "Sohum Shah Mohammad Samad Jyoti Malshe",
        "release_date": "2018-10-12", "vote_average": "8.2", "vote_count": "2600",
        "budget": "60000000", "revenue": "280000000", "runtime": "104", "id": "900015",
        "popularity": "30.1", "tagline": "", "status": "Released",
    },
    {
        "title": "Masaan", "original_title": "Masaan", "original_language": "hi",
        "genres": "Drama Romance", "keywords": "varanasi death grief caste love cremation river",
        "overview": "Intertwining stories of people coping with loss and shame in the holy city of Varanasi by the banks of the Ganges.",
        "director": "Neeraj Ghaywan",
        "cast": "Vicky Kaushal Shweta Tripathi Richa Chadha Sanjay Mishra",
        "release_date": "2015-07-24", "vote_average": "8.1", "vote_count": "1800",
        "budget": "30000000", "revenue": "120000000", "runtime": "110", "id": "900016",
        "popularity": "24.8", "tagline": "", "status": "Released",
    },
    {
        "title": "Article 15", "original_title": "Article 15", "original_language": "hi",
        "genres": "Crime Drama Thriller", "keywords": "caste discrimination india police investigation social justice",
        "overview": "A police officer investigates the disappearance of three dalit girls in a small Indian town and uncovers systemic caste oppression.",
        "director": "Anubhav Sinha",
        "cast": "Ayushmann Khurrana M. Nassar Manoj Pahwa",
        "release_date": "2019-07-05", "vote_average": "8.1", "vote_count": "2200",
        "budget": "120000000", "revenue": "580000000", "runtime": "130", "id": "900017",
        "popularity": "29.3", "tagline": "", "status": "Released",
    },

    # ── MARATHI ─────────────────────────────────────────────────────────────
    {
        "title": "Sairat", "original_title": "Sairat", "original_language": "mr",
        "genres": "Drama Romance", "keywords": "love caste rural maharashtra inter caste marriage",
        "overview": "Two teenagers from different castes in Maharashtra fall in love and face violent consequences from their families and society.",
        "director": "Nagraj Manjule",
        "cast": "Rinku Rajguru Akash Thosar Tanaji Galgunde",
        "release_date": "2016-04-29", "vote_average": "8.3", "vote_count": "1600",
        "budget": "40000000", "revenue": "1000000000", "runtime": "174", "id": "900018",
        "popularity": "27.4", "tagline": "", "status": "Released",
    },
    {
        "title": "Fandry", "original_title": "Fandry", "original_language": "mr",
        "genres": "Drama", "keywords": "caste poverty pig hunt village boy love crush",
        "overview": "A young Dalit boy from Maharashtra tries to hide his family's occupation from his school crush in a searing portrait of caste.",
        "director": "Nagraj Manjule",
        "cast": "Somnat Avghade Rajeshwari Kharat Kishor Kadam",
        "release_date": "2013-02-01", "vote_average": "8.1", "vote_count": "900",
        "budget": "5000000", "revenue": "60000000", "runtime": "104", "id": "900019",
        "popularity": "18.6", "tagline": "", "status": "Released",
    },
    {
        "title": "Natsamrat", "original_title": "Natsamrat", "original_language": "mr",
        "genres": "Drama", "keywords": "theatre actor retirement family tragedy shakespearean",
        "overview": "A legendary Marathi stage actor retires and faces rejection from his family, paralleling characters he played on stage.",
        "director": "Mahesh Manjrekar",
        "cast": "Nana Patekar Medha Manjrekar Vikram Gokhale",
        "release_date": "2016-01-01", "vote_average": "8.3", "vote_count": "1100",
        "budget": "80000000", "revenue": "400000000", "runtime": "163", "id": "900020",
        "popularity": "21.5", "tagline": "", "status": "Released",
    },
    {
        "title": "Shwaas", "original_title": "Shwaas", "original_language": "mr",
        "genres": "Drama Family", "keywords": "grandfather grandson blindness surgery india emotional",
        "overview": "A Marathi grandfather brings his young grandson to the city for eye treatment, only to face a devastating diagnosis.",
        "director": "Sandeep Sawant",
        "cast": "Arun Nalawade Ashwin Chitale Amrita Subhash",
        "release_date": "2004-02-20", "vote_average": "7.9", "vote_count": "600",
        "budget": "3000000", "revenue": "40000000", "runtime": "96", "id": "900021",
        "popularity": "15.2", "tagline": "", "status": "Released",
    },
    {
        "title": "Court", "original_title": "Court", "original_language": "mr",
        "genres": "Drama", "keywords": "courtroom trial folk singer dalit india law social",
        "overview": "An elderly folk singer is arrested for allegedly inciting a sewer worker to suicide, exposing India's archaic legal system.",
        "director": "Chaitanya Tamhane",
        "cast": "Vira Sathidar Vivek Gomber Geetanjali Kulkarni",
        "release_date": "2014-11-21", "vote_average": "8.1", "vote_count": "1200",
        "budget": "8000000", "revenue": "55000000", "runtime": "116", "id": "900022",
        "popularity": "19.3", "tagline": "", "status": "Released",
    },

    # ── TELUGU / TOLLYWOOD ──────────────────────────────────────────────────
    {
        "title": "Baahubali: The Beginning", "original_title": "Baahubali: The Beginning", "original_language": "te",
        "genres": "Action Adventure Drama Fantasy", "keywords": "kingdom war prince epic fantasy india mythology",
        "overview": "In ancient India, an amnesiac warrior discovers his true identity as the lost prince of a powerful kingdom.",
        "director": "S. S. Rajamouli",
        "cast": "Prabhas Rana Daggubati Anushka Shetty Tamannaah",
        "release_date": "2015-07-10", "vote_average": "8.0", "vote_count": "3900",
        "budget": "1800000000", "revenue": "6500000000", "runtime": "159", "id": "900023",
        "popularity": "55.4", "tagline": "", "status": "Released",
    },
    {
        "title": "Baahubali 2: The Conclusion", "original_title": "Baahubali 2: The Conclusion", "original_language": "te",
        "genres": "Action Adventure Drama Fantasy", "keywords": "kingdom betrayal revenge epic prince india mythology",
        "overview": "The conclusion reveals why Kattappa killed Baahubali and how the warrior prince defeats the tyrant king Bhallaladeva.",
        "director": "S. S. Rajamouli",
        "cast": "Prabhas Rana Daggubati Anushka Shetty Tamannaah Sathyaraj",
        "release_date": "2017-04-28", "vote_average": "8.2", "vote_count": "5200",
        "budget": "2500000000", "revenue": "17965000000", "runtime": "167", "id": "900024",
        "popularity": "72.1", "tagline": "", "status": "Released",
    },
    {
        "title": "RRR", "original_title": "RRR", "original_language": "te",
        "genres": "Action Adventure Drama", "keywords": "freedom fighter british colonialism india 1920 epic friendship",
        "overview": "A fictional tale of two legendary Indian freedom fighters — Alluri Sitarama Raju and Komaram Bheem — and their journey before they began fighting for their countries.",
        "director": "S. S. Rajamouli",
        "cast": "N. T. Rama Rao Jr. Ram Charan Ajay Devgn Alia Bhatt",
        "release_date": "2022-03-25", "vote_average": "8.0", "vote_count": "6800",
        "budget": "5500000000", "revenue": "12000000000", "runtime": "187", "id": "900025",
        "popularity": "88.3", "tagline": "", "status": "Released",
    },
    {
        "title": "Arjun Reddy", "original_title": "Arjun Reddy", "original_language": "te",
        "genres": "Drama Romance", "keywords": "love loss surgeon anger self-destruction obsession",
        "overview": "A brilliant but self-destructive surgeon spirals into substance abuse after his college sweetheart is forced to marry someone else.",
        "director": "Sandeep Vanga",
        "cast": "Vijay Deverakonda Shalini Pandey",
        "release_date": "2017-08-25", "vote_average": "8.1", "vote_count": "2400",
        "budget": "50000000", "revenue": "520000000", "runtime": "187", "id": "900026",
        "popularity": "32.6", "tagline": "", "status": "Released",
    },
    {
        "title": "Mahanati", "original_title": "Mahanati", "original_language": "te",
        "genres": "Biography Drama Romance", "keywords": "actress savitri life tragedy celebrity telugu cinema biography",
        "overview": "The life story of legendary Telugu actress Savitri, whose meteoric rise in cinema was followed by a tragic downfall.",
        "director": "Nag Ashwin",
        "cast": "Keerthy Suresh Dulquer Salmaan Samantha Ruth Prabhu",
        "release_date": "2018-05-09", "vote_average": "8.2", "vote_count": "2800",
        "budget": "180000000", "revenue": "850000000", "runtime": "170", "id": "900027",
        "popularity": "34.1", "tagline": "", "status": "Released",
    },
    {
        "title": "Eega", "original_title": "Eega", "original_language": "te",
        "genres": "Action Fantasy Thriller", "keywords": "revenge fly reincarnation insect villain fantasy unique",
        "overview": "A man killed by a ruthless businessman is reincarnated as a housefly and seeks revenge with the help of his beloved.",
        "director": "S. S. Rajamouli",
        "cast": "Nani Samantha Ruth Prabhu Sudeep",
        "release_date": "2012-07-06", "vote_average": "7.9", "vote_count": "2100",
        "budget": "450000000", "revenue": "2000000000", "runtime": "130", "id": "900028",
        "popularity": "28.7", "tagline": "", "status": "Released",
    },
    {
        "title": "Kalki 2898 AD", "original_title": "Kalki 2898 AD", "original_language": "te",
        "genres": "Action Science Fiction Fantasy", "keywords": "dystopian future mythology kalki avatar apocalypse india",
        "overview": "In a dystopian future, a modern warrior is destined to become the final avatar of Vishnu and save humanity.",
        "director": "Nag Ashwin",
        "cast": "Prabhas Deepika Padukone Amitabh Bachchan Kamal Haasan",
        "release_date": "2024-06-27", "vote_average": "7.8", "vote_count": "3200",
        "budget": "6000000000", "revenue": "10000000000", "runtime": "181", "id": "900029",
        "popularity": "65.2", "tagline": "", "status": "Released",
    },

    # ── TAMIL / KOLLYWOOD ───────────────────────────────────────────────────
    {
        "title": "Vikram", "original_title": "Vikram", "original_language": "ta",
        "genres": "Action Crime Thriller", "keywords": "undercover cop drug cartel india vigilante",
        "overview": "A special agent investigates a series of masked killer attacks that target police officers, leading to a larger criminal conspiracy.",
        "director": "Lokesh Kanagaraj",
        "cast": "Kamal Haasan Vijay Sethupathi Fahadh Faasil",
        "release_date": "2022-06-03", "vote_average": "8.4", "vote_count": "4600",
        "budget": "2000000000", "revenue": "4300000000", "runtime": "174", "id": "900030",
        "popularity": "60.8", "tagline": "", "status": "Released",
    },
    {
        "title": "Super Deluxe", "original_title": "Super Deluxe", "original_language": "ta",
        "genres": "Drama Thriller", "keywords": "anthology intertwining stories fate redemption transgender",
        "overview": "Four intertwining stories explore morality, fate, and redemption in contemporary Tamil Nadu.",
        "director": "Thiagarajan Kumararaja",
        "cast": "Vijay Sethupathi Fahadh Faasil Samantha Ruth Prabhu Ramya Krishnan",
        "release_date": "2019-03-29", "vote_average": "8.3", "vote_count": "2700",
        "budget": "300000000", "revenue": "650000000", "runtime": "175", "id": "900031",
        "popularity": "33.5", "tagline": "", "status": "Released",
    },
    {
        "title": "Roja", "original_title": "Roja", "original_language": "ta",
        "genres": "Drama Romance Thriller", "keywords": "kashmir terrorism newlywed wife patriotism india",
        "overview": "A woman travels to Kashmir and fights to free her husband who has been kidnapped by militants.",
        "director": "Mani Ratnam",
        "cast": "Arvind Swamy Madhoo Pankaj Kapur",
        "release_date": "1992-09-18", "vote_average": "7.9", "vote_count": "1400",
        "budget": "20000000", "revenue": "250000000", "runtime": "138", "id": "900032",
        "popularity": "24.3", "tagline": "", "status": "Released",
    },
    {
        "title": "Drishyam 2", "original_title": "Drishyam 2", "original_language": "ml",
        "genres": "Crime Drama Mystery Thriller", "keywords": "family mystery police cover-up crime sequel",
        "overview": "Seven years after a crime was buried, a family faces renewed scrutiny when the original case is reopened.",
        "director": "Jeethu Joseph",
        "cast": "Mohanlal Meena Ansiba Hassan Murali Gopi",
        "release_date": "2021-02-19", "vote_average": "8.4", "vote_count": "3100",
        "budget": "250000000", "revenue": "2600000000", "runtime": "152", "id": "900033",
        "popularity": "44.7", "tagline": "", "status": "Released",
    },
    {
        "title": "KGF Chapter 2", "original_title": "KGF: Chapter 2", "original_language": "kn",
        "genres": "Action Drama Thriller", "keywords": "gold mine power india 1980s gangster rise empire",
        "overview": "Rocky's rise continues as he consolidates control over the Kolar Gold Fields and faces opposition from multiple fronts including the government.",
        "director": "Prashanth Neel",
        "cast": "Yash Sanjay Dutt Raveena Tandon Srinidhi Shetty",
        "release_date": "2022-04-14", "vote_average": "8.2", "vote_count": "7100",
        "budget": "1000000000", "revenue": "12500000000", "runtime": "168", "id": "900034",
        "popularity": "82.4", "tagline": "", "status": "Released",
    },
]

FIELDNAMES = [
    "index", "budget", "genres", "homepage", "id", "keywords", "original_language",
    "original_title", "overview", "popularity", "production_companies",
    "production_countries", "release_date", "revenue", "runtime", "spoken_languages",
    "status", "tagline", "title", "vote_average", "vote_count", "cast", "crew", "director"
]

def run():
    # Backup original
    if not os.path.exists(BACKUP):
        shutil.copy2(CSV_PATH, BACKUP)
        print(f"[OK] Backup saved to {BACKUP}")

    # Read existing rows to get last index and check for duplicates
    existing_titles = set()
    last_index = 0
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_titles.add(row["title"].lower().strip())
            try:
                last_index = max(last_index, int(row["index"]))
            except (ValueError, KeyError):
                pass

    # Filter out already-present movies
    new_movies = [m for m in INDIAN_MOVIES if m["title"].lower().strip() not in existing_titles]
    if not new_movies:
        print("[OK] All Indian movies already present — nothing to add.")
        return

    # Append
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
        for i, m in enumerate(new_movies):
            row = {k: "" for k in FIELDNAMES}
            row.update(m)
            row["index"] = str(last_index + i + 1)
            row["homepage"] = ""
            row["production_companies"] = "[]"
            row["production_countries"] = "[]"
            row["spoken_languages"] = "[]"
            row["crew"] = "[]"
            writer.writerow(row)

    print(f"[OK] Added {len(new_movies)} Indian movies to {CSV_PATH}")

if __name__ == "__main__":
    run()

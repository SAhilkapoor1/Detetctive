import os
import random
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Render Environment Variables
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
PORT = int(os.environ.get("PORT", 10000))

# Dummy HTTP Server taaki Render ka Port requirement satisfy ho jaye
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running via Polling!")

def start_dummy_server():
    server = HTTPServer(('0.0.0.0', PORT), HealthCheckHandler)
    print(f"🌐 Dummy web server listening on port {PORT}...")
    server.serve_forever()

group_solo_cases = {}     
group_solo_players = {}   

FIRST_NAMES = [
    "Aarav", "Vikram", "Natasha", "Kabir", "Meera", "Rohan", "Simran", "Dev", "Ananya", "Zoya", 
    "Karan", "Pooja", "Rahul", "Tanya", "Sameer", "Neha", "Arjun", "Rhea", "Aditya", "Priya", 
    "Manish", "Divya", "Siddharth", "Kavya", "Varun", "Nisha", "Akash", "Shreya", "Kunal", "Tanvi"
]

LAST_NAMES = [
    "Sharma", "Verma", "Singhania", "Kapoor", "Roy", "Mehta", "Malhotra", "Sen", "Deshmukh", "Nayar", 
    "Bose", "Khanna", "Saxena", "Choudhary", "Gupta", "Aggarwal", "Reddy", "Iyer", "Nair", "Patel", 
    "Mehra", "Joshi", "Bhatia", "Chopra", "Tiwari", "Pandey", "Mukherjee", "Banerjee", "Sarin", "Oberoi"
]

PROFESSIONS = [
    "Crypto Billionaire", "Underground Casino Owner", "Genetics Scientist", "Art Collector", "Luxury Hotel Magnate", 
    "Software Architect", "Fashion Tycoon", "Chief Neurosurgeon", "Bollywood Superstar", "Politician & Cabinet Minister", 
    "Defense Arms Dealer", "Real Estate Tycoon", "Hedge-fund Manager", "Renowned Historian", "Cybersecurity Expert"
]

LOCATIONS = [
    "ek high-tech underground bunker", "ek sunehan mahalon jaisi purani haveli", "ek chalte hue private luxury train compartment", "ek secluded beachside glass villa", "ek multi-story cyber corporation tower"
]

WEAPONS = [
    "ek rare neuro-toxin poison", "ek smart-lock electrocution trap", "ek antique silver dagger", "ek custom-built suppressed firearm", "ek heavy obsidian paperweight"
]

ALIBI_ACTIONS = [
    "private network ki encrypted logs audit kar raha tha",
    "security bypass protocol ki firmware testing kar raha tha",
    "ek high-priority overseas client ke sath confidential conference call par tha",
    "restricted perimeter sector mein manual calibration check perform kar raha tha",
    "inventory database ke financial ledger entries reconcile kar raha tha"
]

ALIBI_EXUSES = [
    "aur uska personal device airplane mode par hone ki wajah se koi connection nahi tha.",
    "aur acoustic insulation door lock hone ke karan use koi external disturbance nahi sunai di.",
    "aur security grid ki blind spot zone mein hone ke karan camera frame capture nahi hua.",
    "aur backup generator failure ki wajah se uska digital timestamp temporarily freeze ho gaya tha.",
    "aur physical access control key card server room ke andar lock ho gaya tha."
]

RIDDLE_SUBJECTS = [
    {"ans": "aaina", "adj": ["safed", "chamkila", "chapti"], "desc": ["bina bole sach bolta hai", "apna chehra dikhata hai"]},
    {"ans": "hawa", "adj": ["adhrishya", "thandi", "behti"], "desc": ["sans dene ka kaam karti hai", "dikhti nahi par mehsoos hoti hai"]},
    {"ans": "ghadi", "adj": ["tik-tik karne wali", "gol"], "desc": ["samay batati hai", "suiyon se chalti hai"]},
    {"ans": "kalam", "adj": ["syahi bhari", "patli"], "desc": ["kaagaz par likhne ke kaam aati hai", "sabke shabdon ko roop deti hai"]},
    {"ans": "suraj", "adj": ["garm", "roshni dene wala"], "desc": ["subah aakar andhera mitata hai", "aakash mein chamakta hai"]},
    {"ans": "chand", "adj": ["sheetal", "raat ka raja"], "desc": ["taroon ke beech rehta hai", "raat ko roshni deta hai"]},
    {"ans": "barish", "adj": ["boondon bhari", "aasman se girne wali"], "desc": ["ped-paudhon ki pyas bujhati hai", "dharti ko bhigoti hai"]},
    {"ans": "paani", "adj": ["rangheen", "behne wali"], "desc": ["pyas bujhati hai", "koi aakar nahi hota"]}
]

def generate_endless_riddle():
    subject = random.choice(RIDDLE_SUBJECTS)
    templates = [
        f"Aise kaunsi cheez hai jo {subject['desc'][0]} aur {subject['desc'][1]}?",
        f"Main ek {subject['adj'][0]} cheez hoon jo {subject['desc'][0]} karti hai. Batao main kaun hoon?",
        f"Jise {subject['desc'][1]} kehte hain aur jo hamesha {subject['adj'][1]} hoti hai, batao woh kya hai?"
    ]
    return {
        "q": random.choice(templates),
        "ans": subject["ans"]
    }

def generate_procedural_case():
    victim_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    victim_prof = random.choice(PROFESSIONS)
    location = random.choice(LOCATIONS)
    weapon = random.choice(WEAPONS)
    
    complexity_name = "Infinite Procedural Alibi & Hardcore Forensic Telegram Mode"
    time_limit = 480
    
    num_suspects = 5 
    all_names = [f"{f} {l}" for f in FIRST_NAMES for l in LAST_NAMES]
    suspect_names_pool = random.sample([n for n in all_names if n != victim_name], num_suspects)
    
    roles = ["Business Partner", "Secret Rival", "Ex-Lover / Spouse", "Disgruntled Employee", "Shadowy Informant"]
    random.shuffle(roles)
    
    suspects = {}
    time_slots = ["10:00 PM - 10:15 PM", "10:15 PM - 10:30 PM", "10:30 PM - 10:45 PM", "10:45 PM - 11:00 PM", "11:00 PM - 11:15 PM"]
    
    for i in range(num_suspects):
        name = suspect_names_pool[i]
        role = roles[i]
        timeslot = time_slots[i]
        
        action_str = random.choice(ALIBI_ACTIONS)
        excuse_str = random.choice(ALIBI_EXUSES)
        procedural_alibi = f"Dawa karta hai ki woh time-slot {timeslot} ke dauran {location} ke ek isolated compartment mein akela baithkar {action_str}, {excuse_str}"
        
        suspects[name.lower()] = {
            "name": name,
            "role": role,
            "alibi": procedural_alibi,
            "timeslot": timeslot
        }
    
    culprit_key = random.choice(list(suspects.keys()))
    culprit_info = suspects[culprit_key]
    culprit_timeslot = culprit_info["timeslot"]

    innocent_keys = [k for k in suspects.keys() if k != culprit_key]
    decoy_suspect = suspects[random.choice(innocent_keys)]

    dossier_reports = [
        f"""🔬 **DOSSIER REPORT #01: PATHOLOGICAL & TANATOLOGICAL EVALUATION**
• **Post-mortem interval (PMI)** estimation established the time of death squarely within **{culprit_timeslot}**.
• **Algor mortis** dissipation rate combined with **livor mortis (hypostasis)** patterns and **rigor mortis** fixation indicates active interference.
• Autopsy protocol reveals **petechial hemorrhages** in ocular conjunctiva, localized **ecchymosis**, and micro-contusion mapping. 
• **Histopathological examination** confirms acute asphyxiation markers via {weapon}.
• ⚠️ **Forensic Warning:** **{decoy_suspect['name']}** exhibits surface contamination, serving as a classic **decoy trace**.""",

        f"""🧬 **DOSSIER REPORT #02: TRACE EVIDENCE & BIO-CHEMICAL SPECTROSCOPY**
• **Gas chromatography-mass spectrometry (GC-MS)** and **FTIR** performed on {weapon} residues confirm high-concentration compound traces.
• **Touch DNA** and **STR analysis** yielded degraded **epithelial cells** mixed with synthetic micro-fibers.
• **Dactyloscopy** via **AFIS** cross-referencing identified smeared **papillary ridge patterns**.
• **Toxicology screen** via **LC-MS/MS** isolated systemic neurotoxin markers.
• **Bloodstain pattern analysis (BPA)** and **luminol reaction** traces verify close-proximity kinetic execution.""",

        f"""💻 **DOSSIER REPORT #03: DIGITAL FORENSICS & ALIBI CORROBORATION MATRIX**
• **Digital forensics** and **metadata analysis** confirm an anomalous **SHA-256 cryptographic hash** execution.
• **Volatile memory dump (RAM forensic analysis)** exposed a targeted override routine overlapping with **{culprit_timeslot}**.
• **Timeline reconstruction** and **alibi corroboration matrix** cross-referencing dissolves conflicting statements."""
    ]

    return {
        "victim_name": victim_name,
        "victim_prof": victim_prof,
        "location": location,
        "weapon": weapon,
        "complexity": complexity_name,
        "time_limit": time_limit,
        "suspects": suspects,
        "culprit": culprit_key,
        "dossier": dossier_reports,
        "created_at": time.time()
    }

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name or "Detective"

    group_solo_cases[chat_id] = generate_procedural_case()
    if chat_id not in group_solo_players:
        group_solo_players[chat_id] = {}

    group_solo_players[chat_id][user_id] = {
        "user_name": user_name,
        "pending_riddle": None
    }

    case = group_solo_cases[chat_id]
    suspect_list_text = "\n".join([f"• **{s['name']}** — *{s['role']}* (Alibi Slot: {s['timeslot']})" for s in case["suspects"].values()])
    minutes_given = case["time_limit"] // 60

    text = (
        f"🚨 **INFINITE PROCEDURAL MYSTERY CASE** 🚨 (Detective: {user_name})\n"
        f"📊 Difficulty: {case['complexity']}\n"
        f"⏱️ Time Limit: {minutes_given} Minutes\n"
        f"👤 Mritak: {case['victim_name']} ({case['victim_prof']})\n"
        f"📍 Jagah: {case['location']}\n"
        f"🔪 Hathyar: {case['weapon']}\n\n"
        f"**5 Suspects:**\n{suspect_list_text}\n\n"
        f"💡 Commands:\n"
        f"/examine - Crime scene report (Riddle Locked)\n"
        f"/interrogate [Full Name] - Suspect alibi (Riddle Locked)\n"
        f"/arrest [Full Name] - Arrest culprit"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def examine_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if chat_id not in group_solo_cases or user_id not in group_solo_players.get(chat_id, {}):
        await update.message.reply_text("❌ Pehle /start dabakar naya case shuru karein!")
        return

    riddle = generate_endless_riddle()
    group_solo_players[chat_id][user_id]["pending_riddle"] = {
        "action": "examine",
        "target": None,
        "ans": riddle["ans"]
    }

    text = (
        f"🔒 **DOSSIER ACCESS LOCKED BY PROCEDURAL FIREWALL!**\n\n"
        f"🧩 Riddle: '{riddle['q']}'\n\n"
        f"✏️ Seedha chat mein iska jawab type karein file unlock karne ke liye."
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def interrogate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text("❌ Kisse poochhtach karni hai? Likho: `/interrogate Aarav Sharma`", parse_mode="Markdown")
        return

    suspect_query = " ".join(context.args).lower()

    if chat_id not in group_solo_cases or user_id not in group_solo_players.get(chat_id, {}):
        await update.message.reply_text("❌ Pehle /start game shuru karo!")
        return

    case = group_solo_cases[chat_id]
    if suspect_query not in case["suspects"]:
        valid_names = ", ".join([s['name'] for s in case['suspects'].values()])
        await update.message.reply_text(f"❌ Is naam ka koi suspect nahi hai. Inme se choose karo: {valid_names}")
        return

    riddle = generate_endless_riddle()
    group_solo_players[chat_id][user_id]["pending_riddle"] = {
        "action": "interrogate",
        "target": suspect_query,
        "ans": riddle["ans"]
    }

    text = (
        f"🔒 **ALIBI ACCESS LOCKED BY PROCEDURAL FIREWALL!**\n\n"
        f"🧩 Riddle: '{riddle['q']}'\n\n"
        f"✏️ Seedha chat mein iska jawab type karein alibi kholne ke liye."
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def arrest_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text("❌ Kise arrest karna hai? Likho: `/arrest [Pura Naam]`", parse_mode="Markdown")
        return

    culprit_guess = " ".join(context.args).lower()

    if chat_id not in group_solo_cases or user_id not in group_solo_players.get(chat_id, {}):
        await update.message.reply_text("❌ Pehle /start likhkar game shuru karein!")
        return

    case = group_solo_cases[chat_id]
    real_culprit_name = case["suspects"][case["culprit"]]["name"]

    if culprit_guess == case["culprit"]:
        await update.message.reply_text(f"🏆 **MASTER DETECTIVE! MASTERMIND CAUGHT SUCCESSFULLY!**\n\n**{real_culprit_name}** hi asli kaatil tha! 🎉")
        group_solo_cases.pop(chat_id, None)
        group_solo_players.pop(chat_id, None)
    else:
        await update.message.reply_text(f"❌ **WRONG ARREST!** Galat pakda gaya. Asli mastermind **{real_culprit_name}** tha! Caseover.")
        group_solo_players[chat_id].pop(user_id, None)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if chat_id not in group_solo_cases or user_id not in group_solo_players.get(chat_id, {}):
        return

    player_data = group_solo_players[chat_id][user_id]
    if player_data.get("pending_riddle"):
        riddle_obj = player_data["pending_riddle"]
        ans_input = update.message.text.strip().lower()

        if ans_input == riddle_obj["ans"]:
            player_data["pending_riddle"] = None
            await update.message.reply_text("✨ **RIDDLE SOLVED SUCCESSFULLY!** Access granted.")

            case = group_solo_cases[chat_id]
            if riddle_obj["action"] == "examine":
                for report in case["dossier"]:
                    await update.message.reply_text(report, parse_mode="Markdown")
            elif riddle_obj["action"] == "interrogate":
                s_query = riddle_obj["target"]
                s = case["suspects"][s_query]
                await update.message.reply_text(f"🗣️ **{s['name']} ({s['role']} | Time Slot: {s['timeslot']}):** \n'{s['alibi']}'", parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ **Galat jawab!** Procedural firewall active hai, dimaag lagao aur sahi jawab dobara type karo.")

def main():
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set!")
        return

    server_thread = threading.Thread(target=start_dummy_server, daemon=True)
    server_thread.start()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("examine", examine_command))
    app.add_handler(CommandHandler("interrogate", interrogate_command))
    app.add_handler(CommandHandler("arrest", arrest_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("🤖 Telegram Bot is running in Polling mode with port binding...")
    app.run_polling()

if __name__ == "__main__":
    main()

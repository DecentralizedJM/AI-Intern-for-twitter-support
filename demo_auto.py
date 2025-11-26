#!/usr/bin/env python3
"""
Quick demo of the Twitter Support Bot - Auto-run version
"""
from twitter_handler import handler
from colorama import init, Fore
import time

init(autoreset=True)

def demo():
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}  Twitter Support Bot - Automated Demo")
    print(f"{Fore.CYAN}{'='*70}\n")
    
    scenarios = [
        {
            "title": "Scenario 1: New Complaint",
            "username": "angry_user",
            "message": "My withdrawal is stuck for 3 days! This is unacceptable!",
            "is_dm": False
        },
        {
            "title": "Scenario 2: User Has Ticket",
            "username": "patient_user",
            "message": "I've raised a ticket but no response yet",
            "is_dm": False
        },
        {
            "title": "Scenario 3: DM with Ticket Number (ESCALATION)",
            "username": "patient_user",
            "message": "My ticket number is #12345",
            "is_dm": True
        },
        {
            "title": "Scenario 4: Follow-up/Stalking",
            "username": "angry_user",
            "message": "It's been 2 hours! When will you fix this?",
            "is_dm": False
        },
        {
            "title": "Scenario 5: Credentials Shared (Security Warning)",
            "username": "naive_user",
            "message": "My email is user@gmail.com and password is 1234, please help!",
            "is_dm": False
        },
        {
            "title": "Scenario 6: General Question",
            "username": "curious_user",
            "message": "How do I enable 2FA on Mudrex?",
            "is_dm": False
        },
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{Fore.MAGENTA}{'='*70}")
        print(f"{Fore.MAGENTA}{scenario['title']}")
        print(f"{Fore.MAGENTA}{'='*70}")
        
        print(f"\n{Fore.YELLOW}From: @{scenario['username']}")
        print(f"{Fore.YELLOW}Type: {'DM' if scenario['is_dm'] else 'Public Tweet'}")
        print(f"{Fore.WHITE}Message: \"{scenario['message']}\"")
        
        result = handler.process_message(
            username=scenario['username'],
            message=scenario['message'],
            is_dm=scenario['is_dm']
        )
        
        print(f"\n{Fore.GREEN}✅ Bot Response: \"{result['response']}\"")
        
        if result['escalated']:
            print(f"\n{Fore.RED}🚨 ESCALATED TO SLACK!")
            print(f"{Fore.RED}   Ticket #{result['ticket_number']} flagged for priority support")
        
        print(f"\n{Fore.CYAN}📊 Intent: {result['intent']}")
        time.sleep(1)
    
    print(f"\n{Fore.GREEN}{'='*70}")
    print(f"{Fore.GREEN}✅ Demo Complete!")
    print(f"{Fore.GREEN}{'='*70}\n")
    
    print(f"{Fore.CYAN}Key Features Demonstrated:")
    print(f"  ✅ Empathetic responses to complaints")
    print(f"  ✅ Asking for ticket numbers via DM")
    print(f"  ✅ Auto-escalation to Slack when ticket shared")
    print(f"  ✅ De-escalating impatient users")
    print(f"  ✅ Security warnings for credential sharing")
    print(f"  ✅ FAQ links for general questions")
    print(f"  ✅ Different response variations (no repetition)")
    print(f"\n{Fore.YELLOW}📁 All conversations stored in: data/conversations.db")
    print(f"{Fore.YELLOW}🔧 To test manually: python test_bot.py")
    print(f"{Fore.YELLOW}🌐 To start API server: python webhook_server.py\n")

if __name__ == "__main__":
    demo()

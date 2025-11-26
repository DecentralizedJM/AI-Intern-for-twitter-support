#!/usr/bin/env python3
"""
Interactive CLI for testing Twitter Support Bot
Simulates Twitter mentions and DMs without needing API access
"""
import sys
from colorama import init, Fore, Style
from twitter_handler import handler
from database import db

# Initialize colorama
init(autoreset=True)


def print_banner():
    """Print welcome banner"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}  Twitter Support Bot - Testing Interface")
    print(f"{Fore.CYAN}  Mock Mode (No Twitter API needed)")
    print(f"{Fore.CYAN}{'='*60}\n")


def print_menu():
    """Print main menu"""
    print(f"\n{Fore.YELLOW}Options:")
    print(f"{Fore.GREEN}1. Simulate Tweet (Public Mention)")
    print(f"{Fore.GREEN}2. Simulate DM (Direct Message)")
    print(f"{Fore.GREEN}3. View Conversation History")
    print(f"{Fore.GREEN}4. View User Stats")
    print(f"{Fore.GREEN}5. Test Scenarios (Predefined)")
    print(f"{Fore.RED}6. Exit")
    print()


def simulate_tweet():
    """Simulate a public tweet mention"""
    print(f"\n{Fore.CYAN}--- Simulate Public Tweet ---")
    username = input(f"{Fore.WHITE}Username (without @): ").strip()
    message = input(f"{Fore.WHITE}Tweet message: ").strip()
    
    if not username or not message:
        print(f"{Fore.RED}Username and message are required!")
        return
    
    result = handler.process_message(
        username=username,
        message=message,
        is_dm=False,
        tweet_url=f"https://twitter.com/{username}/status/123456789"
    )
    
    print(f"\n{Fore.GREEN}✅ Bot would reply:")
    print(f"{Fore.WHITE}{result['response']}")


def simulate_dm():
    """Simulate a direct message"""
    print(f"\n{Fore.CYAN}--- Simulate Direct Message ---")
    username = input(f"{Fore.WHITE}Username (without @): ").strip()
    message = input(f"{Fore.WHITE}DM message: ").strip()
    
    if not username or not message:
        print(f"{Fore.RED}Username and message are required!")
        return
    
    result = handler.process_message(
        username=username,
        message=message,
        is_dm=True
    )
    
    print(f"\n{Fore.GREEN}✅ Bot would reply via DM:")
    print(f"{Fore.WHITE}{result['response']}")
    
    if result['escalated']:
        print(f"{Fore.MAGENTA}🚨 Ticket escalated to Slack!")


def view_history():
    """View conversation history for a user"""
    print(f"\n{Fore.CYAN}--- Conversation History ---")
    username = input(f"{Fore.WHITE}Username (without @): ").strip()
    
    if not username:
        print(f"{Fore.RED}Username is required!")
        return
    
    history = db.get_conversation_history(username, limit=10)
    
    if not history:
        print(f"{Fore.YELLOW}No conversations found for @{username}")
        return
    
    print(f"\n{Fore.GREEN}Recent conversations for @{username}:\n")
    for i, conv in enumerate(history, 1):
        dm_label = "[DM]" if conv['is_dm'] else "[Tweet]"
        print(f"{Fore.CYAN}{i}. {dm_label} {conv['created_at']}")
        print(f"   {Fore.WHITE}User: {conv['message']}")
        print(f"   {Fore.GREEN}Bot: {conv['response']}")
        print(f"   {Fore.YELLOW}Intent: {conv['intent']}")
        if conv['ticket_number']:
            print(f"   {Fore.MAGENTA}Ticket: #{conv['ticket_number']}")
        print()


def view_user_stats():
    """View stats for a specific user"""
    print(f"\n{Fore.CYAN}--- User Stats ---")
    username = input(f"{Fore.WHITE}Username (without @): ").strip()
    
    if not username:
        print(f"{Fore.RED}Username is required!")
        return
    
    state = db.get_user_state(username)
    
    if not state:
        print(f"{Fore.YELLOW}No data found for @{username}")
        return
    
    print(f"\n{Fore.GREEN}Stats for @{username}:")
    print(f"  Last Intent: {state['last_intent']}")
    print(f"  Ticket Number: {state['ticket_number'] or 'N/A'}")
    print(f"  Last Interaction: {state['last_interaction']}")
    print(f"  Escalations: {state['escalation_count']}")


def test_scenarios():
    """Run predefined test scenarios"""
    print(f"\n{Fore.CYAN}--- Running Test Scenarios ---\n")
    
    scenarios = [
        {
            "name": "New Complaint",
            "username": "angry_user",
            "message": "My withdrawal is stuck for 3 days! This is unacceptable!",
            "is_dm": False
        },
        {
            "name": "User Has Ticket",
            "username": "patient_user",
            "message": "I've raised a ticket but no response yet",
            "is_dm": False
        },
        {
            "name": "DM with Ticket Number",
            "username": "patient_user",
            "message": "My ticket number is #12345",
            "is_dm": True
        },
        {
            "name": "Follow-up/Stalking",
            "username": "angry_user",
            "message": "It's been 2 hours since I messaged! When will you fix this?",
            "is_dm": False
        },
        {
            "name": "Credentials Shared",
            "username": "naive_user",
            "message": "My email is user@gmail.com and password is 1234, please help!",
            "is_dm": False
        },
        {
            "name": "General Question",
            "username": "curious_user",
            "message": "How do I enable 2FA on Mudrex?",
            "is_dm": False
        },
        {
            "name": "DM Follow-up",
            "username": "patient_user",
            "message": "Any update on my ticket?",
            "is_dm": True
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"{Fore.MAGENTA}Scenario {i}: {scenario['name']}")
        print(f"{Fore.CYAN}{'─'*50}")
        
        result = handler.process_message(
            username=scenario['username'],
            message=scenario['message'],
            is_dm=scenario['is_dm']
        )
        
        print()
        input(f"{Fore.YELLOW}Press Enter for next scenario...")
        print()


def main():
    """Main CLI loop"""
    print_banner()
    
    while True:
        print_menu()
        choice = input(f"{Fore.YELLOW}Select option (1-6): ").strip()
        
        if choice == "1":
            simulate_tweet()
        elif choice == "2":
            simulate_dm()
        elif choice == "3":
            view_history()
        elif choice == "4":
            view_user_stats()
        elif choice == "5":
            test_scenarios()
        elif choice == "6":
            print(f"\n{Fore.GREEN}Thanks for testing! 👋\n")
            sys.exit(0)
        else:
            print(f"{Fore.RED}Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Interrupted. Goodbye! 👋\n")
        sys.exit(0)

from file import get_ai_msg

def main():
    patient_prompt = input("Enter the patient prompt: ")
    ai_msg = get_ai_msg(patient_prompt)
    print(ai_msg)
    


if __name__ == "__main__":
    main()

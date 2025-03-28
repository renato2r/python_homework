import traceback

try:
      with open('diary.txt','a') as file:
            first_prompt = True
            while True:

                  if first_prompt:
                        answer = input("What happened today? (Type 'done for now' to exit)")
                        first_prompt = False
                  else:
                        answer = input("What else? (Type 'done for now' to exit) ")
                  if answer.lower() == 'done for now':
                        break

                  file.write(answer + '\n')
            
except Exception as e:
      print('An exception ocurred.')
      print (f'Exception type: {type(e).__name__}')
      traceback.print_exc()       
        

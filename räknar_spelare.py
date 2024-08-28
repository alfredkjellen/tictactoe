import importlib

def lägg_till_spelare():
    with open('antal_spelare.py', 'r') as file:
        lines = file.readlines()
        
    for i, line in enumerate(lines):
        just_nu = int(line.split('=')[1].strip())
        nytt_värde = just_nu + 1
        lines[i] = f'antal_spelare = {nytt_värde}'
        break
    
    with open('antal_spelare.py', 'w') as file:
        file.writelines(lines)
    
def hämta_nuvarande_antal():
    import antal_spelare
    importlib.reload(antal_spelare)
    return antal_spelare.antal_spelare

print(f'antal spelare: {hämta_nuvarande_antal()}')
lägg_till_spelare()
print(f'antal spelare: {hämta_nuvarande_antal()}')
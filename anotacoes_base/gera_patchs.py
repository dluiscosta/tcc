#gera 1 patch aleatório posicionado dentro da lâmina para cada uma das imagens cuja lâmina já foi anotada

import dill
dill.load_session(r'anotacoes_base\patchs.pkl')

import random
for i in range(1, 129):
    if laminas[i] is not None:
        random.seed(i)
        patch = Patch()
        patch.canto_sup_esq = (random.randint(0, 3120), random.randint(0, 4160))
        while not laminas[i].patchEstaDentro(patch):
            patch.canto_sup_esq = (random.randint(0, 3120), random.randint(0, 4160))

dill.dump_session(r'anotacoes_base\patchs.pkl')
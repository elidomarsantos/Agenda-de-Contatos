
from logging import root
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.uix.list import OneLineListItem
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from plyer import call
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons
from kivy.properties import StringProperty
import json
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.datatables import MDDataTable




class ListItemWithCheckbox(OneLineAvatarIconListItem):
    '''Custom list item.'''

    icon = StringProperty("account-box-multiple")
    screen_manager = ObjectProperty() 

class RightCheckbox(IRightBodyTouch, MDCheckbox):
    '''Custom right container.'''    
    

class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class Ministerio_por_Telefone(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange"
        return Builder.load_file('main.kv')
        

    def consulta(self):
        prefixo = self.root.ids.prefixo.text
        #prefixo = int(prefixo1)
        telefone1 = self.root.ids.telefone.text
        telefone = int(telefone1)
        quantidade1 = self.root.ids.quantidade.text
        quantidade = int(quantidade1)
        for i in range(quantidade):
            telefone2 = telefone + i
            self.root.ids.lista_numeros.add_widget(ListItemWithCheckbox(text=f'{telefone2}', on_press= self.vai_pra_ficha))
            self.store = JsonStore('contatos.json')
            self.store.put(telefone2, pref=prefixo, name='', obs='', lig='')

    


    def vai_pra_ficha(self, ListItemWithCheckbox):
        telefone = ListItemWithCheckbox.text
        self.root.ids.ficha_telefone.text = (f'{telefone}')
        self.root.ids.escolha_numero.text = (f'Número:  {telefone},  confirma?')
        self.root.ids.escolha_numero1.text = (f'Número: {telefone},  confirma?')
        self.root.ids.escolha_numero2.text = (f'Número: {telefone}, confirma?')
        if self.store.exists(telefone):
            ident = self.store.get(telefone)['name']
            obs = self.store.get(telefone)['obs']
            pref = self.store.get(telefone)['pref']
            self.root.ids.ficha_nome.text = (f'{ident}')
            self.root.ids.ficha_obs.text = (f'{obs}')  
            self.root.ids.ficha_prefixo.text = (f'{pref}') 
       
                
    def efetuadas(self):
        telefone = self.root.ids.ficha_telefone.text
        self.store1 = JsonStore('ja_ligou.json')
        self.store1.put(telefone, lig='sim')

    def revisita(self):
        
        telefone = self.root.ids.ficha_telefone.text
        self.store2 = JsonStore('revisita.json')
        self.store2.put(telefone, rev='sim')

    def salvar_na_lista(self):
        prefixo = self.root.ids.ficha_prefixo.text
        telefone = self.root.ids.ficha_telefone.text
        nome = self.root.ids.ficha_nome.text
        observacoes = self.root.ids.ficha_obs.text
        self.store.put(telefone, pref=prefixo, name=nome, obs=observacoes)
           
    def on_start(self):
        self.store = JsonStore('contatos.json')
        self.store1 = JsonStore('ja_ligou.json')
        self.store2 = JsonStore('revisita.json')
        for item in self.store:
            if item in self.store1:
                if item not in self.store2:
                    self.root.ids.lista_numeros1.add_widget(ListItemWithCheckbox(text=f'{item}', on_release= self.vai_pra_ficha))
        
        for item_not in self.store:
            if item_not not in self.store1:
                    self.root.ids.lista_numeros.add_widget(ListItemWithCheckbox(text=f'{item_not}', on_release= self.vai_pra_ficha))
                
        for rev in self.store2:
                self.root.ids.lista_numeros2.add_widget(ListItemWithCheckbox(text=f'{rev}', on_release= self.vai_pra_ficha))

    def del_store(self):
        self.store = JsonStore('contatos.json')
        for key in self.store.keys():
           self.store.delete(key)
        self.store1 = JsonStore('ja_ligou.json')
        for key in self.store1.keys():
            self.store1.delete(key)
        self.store2 = JsonStore('revisita.json')
        for key in self.store2.keys():
            self.store2.delete(key)



    def abrir_telefone(self):
      
        tel = self.root.ids.ficha_telefone.text
        prefixo = self.root.ids.ficha_prefixo.text
        telefone = prefixo+tel
        call.makecall(tel=telefone)

 
    

Ministerio_por_Telefone().run()
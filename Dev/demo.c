#include "midi.c"

void ecrire_piste1(FILE *fichier) {   
    unsigned long marque = MIDI_ecrire_en_tete_piste(fichier) ;
    MIDI_tempo(fichier, 500000) ;   
    MIDI_fin_de_la_piste(fichier) ;
    ecrire_taille_finale_piste(fichier, marque) ;    
}

void ecrire_piste2(FILE *fichier) {
    unsigned long marque = MIDI_ecrire_en_tete_piste(fichier) ;
    
    MIDI_Program_Change(fichier, 0, 90) ;
    for(int i=C3 ; i<=C3+12 ; i=i+1){
        Note_unique_avec_duree(fichier, 0, i, 64, noire/2) ;        
    }
    
    for(int i=0 ; i<=127 ; i=i+1){
        MIDI_Program_Change(fichier, 0, i) ;
        Note_unique_avec_duree(fichier, 0, C3 + 9, 64, noire) ;        
    }
    
    MIDI_fin_de_la_piste(fichier) ;
    ecrire_taille_finale_piste(fichier, marque) ;    
}

int main(void) {
    FILE *fichier_midi = fopen("demo.mid", "wb") ;
    MIDI_ecrire_en_tete(fichier_midi, 1, 2, noire) ;
    ecrire_piste1(fichier_midi) ;
    ecrire_piste2(fichier_midi) ; 
    fclose(fichier_midi) ;  
}
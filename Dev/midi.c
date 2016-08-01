// Vincent MAGNIN, 16/02/2016, Création d'un fichier MIDI, GPLv3

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define noire 128
#define ON  0x90
#define OFF 0x80
#define C3  60
#define percu 9
#define reverb 0x5B
#define chorus 0x5D
#define phaser 0x5F

void ecrire_variable_length_quantity(FILE *fichier, unsigned long i) {
    bool continuer ;

    if (i > 0x0FFFFFFF) {
        printf("ERREUR : delai > 0x0FFFFFFF ! \n") ;
        exit(EXIT_FAILURE) ;
    }
    
    unsigned long filo = i & 0x7F ;
    i = i >> 7 ;
    while (i != 0) {
        filo = (filo << 8)  + ((i & 0x7F) | 0x80) ;
        i = i >> 7 ;
    }
    
    do {
        fwrite(&filo, 1, 1, fichier) ;
        continuer = filo & 0x80 ;
        if (continuer) filo = filo >> 8 ;
    } while (continuer) ;    
}

void MIDI_delta_time(FILE *fichier, unsigned long duree) {
    ecrire_variable_length_quantity(fichier, duree) ;
}
    
void MIDI_ecrire_en_tete(FILE *fichier, unsigned char SMF, unsigned short pistes, unsigned short nbdiv) {  
    if ((SMF == 0) && (pistes > 1)) {
        printf("ERREUR : une seule piste possible en SMF 0 ! \n") ;
        exit(EXIT_FAILURE) ;
    }

    unsigned char octets[14] = {0x4d, 0x54, 0x68, 0x64, 0x00, 0x00, 0x00, 0x06} ;
    octets[8]  = 0 ;
    octets[9]  = SMF ;
    octets[10] = pistes >> 8 ; 
    octets[11] = pistes ;  
    octets[12] = nbdiv  >> 8 ; 
    octets[13] = nbdiv ;     // Nombre de divisions de la noire
    fwrite(&octets, 14, 1, fichier) ;
}

void MIDI_tempo(FILE *fichier, unsigned long duree) {
    MIDI_delta_time(fichier, 0) ;
    unsigned char octets[6] = {0xFF, 0x51, 0x03} ;
    octets[3] = duree >> 16 ;
    octets[4] = duree >> 8 ;
    octets[5] = duree ;
    fwrite(&octets, 6, 1, fichier) ;
}

void MIDI_Program_Change(FILE *fichier, unsigned char canal, unsigned char instrument) {
    unsigned char octets[2] ;
    MIDI_delta_time(fichier, 0) ;
    octets[0] = 0xC0 + canal % 16 ;
    octets[1] = instrument % 128 ;
    fwrite(&octets, 2, 1, fichier) ;
}

void MIDI_Control_Change(FILE *fichier, unsigned char canal, unsigned char type, unsigned char valeur) {
    unsigned char octets[3] ;
    MIDI_delta_time(fichier, 0) ;
    octets[0] = 0xB0 + canal % 16 ;
    octets[1] = type % 128 ;
    octets[2] = valeur % 128 ;
    fwrite(&octets, 3, 1, fichier) ;
}

void MIDI_Note(unsigned char etat, FILE *fichier, unsigned char canal, unsigned char Note_MIDI, unsigned char velocite) {
    unsigned char octets[3] ;
    octets[0] = etat + canal % 16 ;
    octets[1] = Note_MIDI % 128 ;
    octets[2] = velocite % 128 ;
    fwrite(&octets, 3, 1, fichier) ;
}

void Note_unique_avec_duree(FILE *fichier, unsigned char canal, unsigned char Note_MIDI, unsigned char velocite, unsigned long duree) {
    MIDI_delta_time(fichier, 0) ;
    MIDI_Note(ON,  fichier, canal, Note_MIDI, velocite) ; 
    MIDI_delta_time(fichier, duree) ;
    MIDI_Note(OFF, fichier, canal, Note_MIDI, 0) ;
}

unsigned long MIDI_ecrire_en_tete_piste(FILE *fichier) {
    unsigned char octets[8] = {0x4d, 0x54, 0x72, 0x6b, 0x00, 0x00, 0x00, 0x00} ;
    fwrite(&octets, 8, 1, fichier) ;
    return ftell(fichier) ;
}

void MIDI_fin_de_la_piste(FILE *fichier) {
    MIDI_delta_time(fichier, 0) ;
    unsigned char octets[3] = {0xFF, 0x2F, 0x00} ;
    fwrite(&octets, 3, 1, fichier) ;
}

void ecrire_taille_finale_piste(FILE *fichier, unsigned long marque) {
    unsigned char octets[4] ;
    unsigned long taille = ftell(fichier) - marque ;
    fseek(fichier, marque-4, SEEK_SET) ;    // On rembobine
    octets[0] = taille >> 24 ; 
    octets[1] = taille >> 16 ; 
    octets[2] = taille >> 8 ; 
    octets[3] = taille ;
    fwrite(&octets, 4, 1, fichier) ;
    fseek(fichier, 0, SEEK_END) ;
}
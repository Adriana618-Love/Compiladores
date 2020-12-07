digito [0-9]
ws [ \t]+
alpha [a-zA-Z]
entero {digito}+
hora {entero}:{entero}
horario ({alpha}\.[ ]{alpha}\.)
fecha {entero}[/]{entero}[/]{entero}
string  [^\n"\[\]]+
remitente {string}:
destinatario [A-Z]{string}

    void imprimir(char *sToken){
        printf("-%s-",sToken);
    }
    int contador = 0;
    char my_hora[10];
    char my_horario[10];
    char my_fecha[10];
    char my_remitente[20];
    char my_destinatario[100];
    void assing(char* dest, char *sToken){
        strncpy(dest,sToken,strlen(sToken)+1);
        //printf("+%s+%s",sToken,my_hora);
    }

    void latex(){
        char ltx[400]="";
        char cont[10];
        if(contador>10){
            for(int i=0;contador;++i){
                cont[i]=(contador/10)+'0';
                contador/=10; 
            }
        }
        else{
            cont[0]=contador+'0';
        }
        strcat(ltx,"\\begin{tabular}{|c|p{3cm}|p{8cm}|p{2cm}|} \\hline\n");
        strcat(ltx,"\\textsc{");strcat(ltx,my_remitente);strcat(ltx,"} &\n");
        strcat(ltx,cont);strcat(ltx," &\n");
        strcat(ltx,my_destinatario);strcat(ltx," &\n");
        strcat(ltx,"\\begin{tabular}{c}\n");
        strcat(ltx,"\\footnotesize{");strcat(ltx,my_fecha);strcat(ltx,"} \\\\\n");
        strcat(ltx,"\\Large{\\textbf{");strcat(ltx,my_hora);strcat(ltx,"}} \\\\\n");
        strcat(ltx,my_horario);strcat(ltx,"\n");
        strcat(ltx,"\\end{tabular} \\\\\n");
        strcat(ltx,"\\hline\n");
        strcat(ltx,"\\end{tabular}\n");
        printf("%s",ltx);
        memset(my_hora, 0, strlen(my_hora));
        memset(my_horario, 0, strlen(my_horario));
        memset(my_fecha, 0, strlen(my_fecha));
        memset(my_remitente, 0, strlen(my_remitente));
        memset(my_destinatario, 0, strlen(my_destinatario));
    }
%%
[\[] { contador++; }
[,\]]
{hora} {assing(my_hora,yytext);}
{horario} {assing(my_horario,yytext);}
{fecha} {assing(my_fecha,yytext);}
{remitente} {assing(my_remitente,yytext);}
{destinatario} {assing(my_destinatario,yytext);}
[\n] {latex();}
%%
int main(){
    yylex();
}
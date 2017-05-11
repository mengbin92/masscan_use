
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <time.h>
#include <sys/stat.h>
#include <signal.h>
#include <string.h>


void daemon_init(const char* pname,int facility)
{
    int i;
    pid_t pid;
    struct sigaction sa;

    umask(0);
    if((pid = fork()) < 0)
    {
        printf("%s\n","fork() error!!!");
        exit(-1);
    }
    else if(pid > 0)
        exit(0);
    setsid();

    sa.sa_handler = SIG_IGN;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    if(sigaction(SIGHUP,&sa,NULL) < 0 )
    {
        printf("%s\n","sigaction() error!!!");
        exit(-1);
    }
    if((pid = fork()) < 0)
    {
        printf("%s\n","fork() error!!!");
        exit(-1);
    }
    else if(pid > 0)
        exit(0);
    for(i = 0;i<3;++i)
        close(i);

}

int main(int argc,char* argv[])
{
    time_t ticks;
    char buf[1024] = {0};

    daemon_init(argv[0],0);
    while(1)
    {
        /*
        FILE* fp = fopen("~/time.txt","w+");
        ticks = time(NULL);
        snprintf(buf,sizeof(buf),"%.24s\n",ctime(&ticks));
        fwrite(buf,strlen(buf),0,fp);

        fclose(fp);
        */

        system("python3 sql.py");
        sleep(6*3600);
        system("rm -f *.xml");
    }


    return 0;
}

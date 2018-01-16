#!/usr/bin/env python2 -x
# -*- coding: utf-8 -*-

import socket
import string
import random
import ConfigParser
import os.path as path
import sqlite3, datetime

from time import *
from commands import getoutput
from urllib import urlopen
from re import search, sub



def send_priv(user_send, msg):
        s.send("PRIVMSG %s :%s\n" %  (user_send, msg))

def send_notice(user_chan, msg):
        s.send("NOTICE %s :%s\n" % (user_chan, msg))

conexion = sqlite3.connect('database.sql')

consulta = conexion.cursor()

sql = """
CREATE TABLE IF NOT EXISTS test(
id INTEGER PRIMARY KEY NOT NULL,
user VARCHAR(10) NOT NULL,
fecha DATE NOT NULL)"""

sql2 = """
CREATE TABLE IF NOT EXISTS permisos(
id INTEGER PRYMARY KEY NOT NULL,
canal TEXT NOT NULL,
permisos TEXT NOT NULL)
"""

consulta.execute(sql)
consulta.execute(sql2)


consulta.close()
conexion.commit()
conexion.close()

if path.exists('config.ini'):
        config = ConfigParser.ConfigParser()
        config.read(['config.ini'])
        HOST = config.get("config", "host")
        PORT = config.get("config", "port")
        NICK = config.get("config", "nick")
        IDENT = config.get("config", "ident")
        REALNAME = config.get("config", "realname")
        CHAN = config.get("config", "channel") 
else:
        HOST="irc.freenode.net"
        PORT=6667
        NICK="LinelBot-"
        IDENT="LinelBot"
        REALNAME="LinelBot"
        CHAN="###Pruebas"
readbuffer=""
track = ''
NickServ='nickserv'
cfg = ConfigParser.ConfigParser()
FOUNDER='linel'
ModeOp = []
user_registered = None
connection = False
user_fail = []
while connection == False:
        try:
                s=socket.socket()
                s.connect((HOST, int(PORT)))
                s.send("NICK %s\r\n" % NICK)
                s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
                sleep(9)
                s.send("JOIN :%s\r\n" % CHAN)
                connection = True
                print("Conectado.")
                #s.send("PRIVMSG %s :%s\r\n" % (CHAN, "I am Bot"))
                #s.send("PRIVMSG %s :%s\r\n" % (CHAN, "la perfeccion es imperfecta"))
        except socket.gaierror:
                connection = False
                print("No conecto, reconectando...")
        except socket.errno:
                connection = False
                print("No conecto, reconectando...")
                
away = []
woman = False

def user_account(user):
        global readbuffer
        s.send("WHOIS %s\n" % user)
        complet = False
        sleep(0.1)
        while 1:
                readbuffer=readbuffer+s.recv(1024)
                temp_=string.split(readbuffer, "\n")
                readbuffer=temp_.pop( )
                for line_ in temp_:
                        line_=string.rstrip(line_)
                        line_=line_.split()
                        print(line_)
                        if len(line_) > 1:
                                if line_[1] == '311':
                                        continue
                                if line_[1] == '312':
                                        continue
                                if line_[1] == '330':
                                        account = line_[4]
                                        return account
                                        complet=True
                                        break
                                if line_[1] == '401':
                                        s.send("PRIVMSG %s :Error: usuario no encontrado\n" % CHAN_A)
                                        return False
                                        complet=True
                                        break
                                if line_[1] == '318':
                                        s.send("PRIVMSG %s :Error: usuario no logueado en nickserv\n" % CHAN_A)
                                        return False
                                        complet=True
                if complet == True:
                        break

def send_msg(msg):
        s.send("PRIVMSG %s :%s\n" % (CHAN_A, msg))
        print(CHAN_A)
def send_join(chann):
        s.send("JOIN :%s\r\n" % chann)

def send_part(chann):
        s.send("PART %s Saliendo\n" % chann)

def send_mode_op(n):
        op = "o" * long_
        s.send("MODE %s %s %s\n" % (CHAN_A, op, n))

def send_mode_deop(user):
        s.send("MODE %s -o %s\n" % (CHAN_A, user))

def send_mode_voice(user):
        s.send("MODE %s +v %s\n" % (CHAN_A, user))

def send_mode_devoice(user):
        s.send("MODE %s -v %s\n" % (CHAN_A, user))
        print(user)

def register_user(user):
        conexion = sqlite3.connect('database.sql')
        consulta = conexion.cursor()

        user = user_account(user)
        sql1 = "SELECT * FROM test WHERE user = \"%s\"" % user

        if user != False:
                
        
                if consulta.execute(sql1):
                        try:
                                filas = consulta.fetchone()
                                s.send("PRIVMSG %s :El usuario %s ya se encuentra registrado\n" % (CHAN_A, filas[1]))

                        except TypeError:
                                argumentos = (user, datetime.date.today())

                                sql = """INSERT INTO test(user, fecha)
                                VALUES (?, ?)"""

                                if consulta.execute(sql, argumentos):
                                        s.send("PRIVMSG %s :Usuario Registrado con exito\n" % CHAN_A)



        consulta.close()
        conexion.commit()

def set_permisos_op(user):
        conexion = sqlite3.connect('database.sql')
        consulta = conexion.cursor()

        user = user_account(user)
        
        sql1 = "SELECT * FROM test WHERE user=\"%s\"" % user
       
        consulta1 = consulta.execute(sql1)
                
        
        filas = consulta.fetchone()
        
        if user != False:
        
                try:
                        sql2 = "SELECT * FROM permisos WHERE id = %s" % filas[0]
                        print(user)
                        if consulta.execute(sql2):
                               filas1 = consulta.fetchone()
                               if "op" in filas1[2] and filas1[1] == CHAN_A:
                                       s.send("PRIVMSG %s :Error el usuario ya posee estos permisos\n" % CHAN_A)
                               elif filas1[2] == "voice":
                                       sql4 = "UPDATE permisos SET permisos = \"op-voice\" WHERE id = %s" % filas[0]
                                       consulta.execute(sql4)
                                       s.send("PRIVMSG %s :Permisos otorgados\n" % CHAN_A)
                               elif not "voice" in filas1[1] and not "op" in filas1[1] and CHAN_A == filas1[1]:
                                       sql5 = "UPDATE permisos SET permisos = \"op\" WHERE id = %s" % filas[0]
                                       consulta.execute(sql5)
                                       s.send("PRIVMSG %s :Permisos otorgados\n" % CHAN_A)

                               else:
                                       argumentos = (filas[0], CHAN_A , "op")
                                       sql3 = "INSERT INTO permisos (id, canal, permisos) VALUES (?, ?, ?)"
                                       consulta.execute(sql3, argumentos)
                                       s.send("PRIVMSG %s :Permisos otorgados\n" % CHAN_A)
                       
                except TypeError:
                        
                        try:
                                argumentos = (filas[0], CHAN_A , "op")
                                sql3 = "INSERT INTO permisos (id, canal, permisos) VALUES (?, ?, ?)"
                                consulta.execute(sql3, argumentos)
                                s.send("PRIVMSG %s :Permisos otorgados\n" % CHAN_A)
                        except TypeError:
                                send_msg("Usuario no registrado")
                

        consulta.close()

        conexion.commit()
        conexion.close()

def drop_permisos_op(user):
        conexion = sqlite3.connect('database.sql')
        consulta = conexion.cursor()

        sql1 = "SELECT * FROM test WHERE user=\"%s\"" % user
       
        consulta1 = consulta.execute(sql1)
                
        
        filas = consulta.fetchone()
        

        

        try:
                sql2 = "SELECT * FROM permisos WHERE id = %s" % filas[0]
                if consulta.execute(sql2):
                       filas1 = consulta.fetchone()
                       if "op" in filas1[2] and filas1[1] == CHAN_A:
                               sql4 = "UPDATE permisos SET permisos = \"voice\" WHERE id = %s" % filas[0]
                               consulta.execute(sql4)
                               s.send("PRIVMSG %s :Permisos removidos\n" % CHAN_A)
                       elif filas1[2] == "voice":
                               s.send("PRIVMSG %s :Error el usuario no tiene estos permisos\n" % CHAN_A)
                       elif filas1[2] == "op":
                               sql5 = "DELETE * FROM permisos = \"op\" WHERE id = %s" % filas[0]
                               consulta.execute(sql5)
                               s.send("PRIVMSG %s :Permisos removidos\n" % CHAN_A)

               
        except TypeError:
               s.send("PRIVMSG %s :Error el usuario no posee estos permisos\n" % CHAN_A)
               

        consulta.close()

        conexion.commit()
        conexion.close()
        

        
def set_permisos_voice(user):
        conexion = sqlite3.connect('database.sql')
        consulta = conexion.cursor()

        sql1 = "SELECT * FROM test WHERE user=\"%s\"" % user
       
        consulta1 = consulta.execute(sql1)
                
        
        filas = consulta.fetchone()
        

        
        try:
                sql2 = "SELECT * FROM permisos WHERE id = %s" % filas[0]
                if consulta.execute(sql2):
                       filas1 = consulta.fetchone()
                       if "voice" in filas1[2] and filas1[1] == CHAN_A:
                               s.send("PRIVMSG %s :Error el usuario ya posee estos permisos\n" % CHAN_A)
                       elif filas1[2] == "op":
                               sql4 = "UPDATE permisos SET permisos = \"op-voice\" WHERE id = %s AND canal = \"%s\"" % (filas[0], CHAN_A)
                               consulta.execute(sql4)
                               s.send("PRIVMSG %s :Permisos otorgados\n" % CHAN_A)
                       elif not "voice" in filas1[1] and not "op" in filas1[1] and CHAN_A == filas1[1]:
                               sql5 = "UPDATE permisos SET permisos = \"op\" WHERE id = %s AND canal = \"%s\"" % (filas[0], CHAN_A)
                               consulta.execute(sql5)
                               s.send("PRIVMSG %s :Permisos otorgados\n" % CHAN_A)

                       else:
                               argumentos = (filas[0], CHAN_A , "op")
                               sql3 = "INSERT INTO permisos (id, canal, permisos) VALUES (?, ?, ?)"
                               consulta.execute(sql3, argumentos)
                               s.send("PRIVMSG %s :Permisos otorgados\n" % CHAN_A)
               
        except TypeError:
               try:
                       argumentos = (filas[0], CHAN_A , "voice")
                       sql3 = "INSERT INTO permisos (id, canal, permisos) VALUES (?, ?, ?)"
                       consulta.execute(sql3, argumentos)
                       s.send("PRIVMSG %s :Permisos otorgados\n" % CHAN_A)
               except TypeError:
                       s.send("PRIVMSG %s :Usuario no registrado\n" % CHAN_A)
               

        consulta.close()

        conexion.commit()
        conexion.close()

def drop_permisos_voice(user):
        conexion = sqlite3.connect('database.sql')
        consulta = conexion.cursor()

        sql1 = "SELECT * FROM test WHERE user=\"%s\"" % user
       
        consulta1 = consulta.execute(sql1)
                
        
        filas = consulta.fetchone()
        

        
        try:
                sql2 = "SELECT * FROM permisos WHERE id = %s" % filas[0]
                if consulta.execute(sql2):
                       filas1 = consulta.fetchone()
                       if "voice" in filas1[2] and filas1[1] == CHAN_A and "op" in filas1[2]:
                               sql4 = "UPDATE permisos SET permisos = \"op\" WHERE id = %s" % filas[0]
                               consulta.execute(sql4)
                               s.send("PRIVMSG %s :Permisos removidos\n" % CHAN_A)
                       elif filas1[2] == "op":
                               s.send("PRIVMSG %s :Error el usuario no tiene estos permisos\n" % CHAN_A)
                       elif filas1[2] == "voice":
                               sql5 = "DELETE * FROM permisos = \"voice\" WHERE id = %s" % filas[0]
                               consulta.execute(sql5)
                               s.send("PRIVMSG %s :Permisos removidos\n" % CHAN_A)
                                
               
        except TypeError:
               s.send("PRIVMSG %s :Error el usuario no esta registrado\n" % CHAN_A)
               

        consulta.close()

        conexion.commit()
        conexion.close()
        

def check_user(user):
        conexion = sqlite3.connect('database.sql')
        consulta = conexion.cursor()
        user = user_account(user)
        sql1 = "SELECT * FROM test WHERE user = \"%s\"" % user
        fila = consulta.fetchone()

        sql2 = "SELECT * FROM test LEFT JOIN permisos ON permisos.id = test.id WHERE user = \"%s\" AND canal = \"%s\"" % (user, CHAN_A)

        if user != False:
                if consulta.execute(sql2):
                        fila1 = consulta.fetchone()
                        try:
                                if fila1[4] == CHAN_A and "op" in fila1[5]:
                                        return True
                                else:
                                        return False
                        except TypeError:
                                return False




        consulta.close()
        conexion.commit()
def check_user_voice(user):
        conexion = sqlite3.connect('database.sql')
        consulta = conexion.cursor()

        sql1 = "SELECT * FROM test WHERE user = \"%s\"" % user
        fila = consulta.fetchone()

        sql2 = "SELECT * FROM test LEFT JOIN permisos ON permisos.id = test.id WHERE user = \"%s\" AND canal = \"%s\"" % (user, CHAN_A)
        
        if consulta.execute(sql2):
                fila1 = consulta.fetchone()
                try:
                        if fila1[4] == CHAN_A and "voice" in fila1[5]:
                                return True
                        else:
                                return False
                except TypeError:
                        return False




        consulta.close()
        conexion.commit()
def moneda():
        moneda = ['cara', 'cruz']
        send_msg('\x01ACTION tira una moneda y sale... \x02%s\x02!\x01' % random.choice(moneda))


def list_op():
        conexion = sqlite3.connect('database.sql')
        consulta = conexion.cursor()
        CHAN1 = CHAN_A
        sql = "SELECT * FROM test LEFT JOIN permisos ON test.id = permisos.id WHERE canal = \"%s\"" % CHAN_A
        
        
        if consulta.execute(sql):
                filas = consulta.fetchall()
                print(filas)
                if filas == []: 
                        s.send("PRIVMSG %s :No hay permisos para ningun usuario en este canal\n" % CHAN_A)
                else:
                        s.send("PRIVMSG %s :Permisos de usuarios en el canal %s\n" % (CHAN_A, CHAN1))
                        s.send("PRIVMSG %s :{:^10}{:^10}{:^20}\n".format('id','usuario', 'permisos') % CHAN_A)
                        
                        for fila in filas:
                                s.send("PRIVMSG %s :{:^10}{:^10}{:^20}\n".format(fila[0],fila[1],fila[5]) % CHAN_A)
        consulta.close()
        conexion.close()
def list_all():
        conexion = sqlite3.connect('database.sql')
        consulta = conexion.cursor()

        sql = "SELECT * FROM test"

        if consulta.execute(sql):
                filas = consulta.fetchall()
                s.send("PRIVMSG %s :id \t usuario\n" % CHAN_A)
                
                for fila in filas:
                        s.send("PRIVMSG %s :%s    %s\n" % (CHAN_A, fila[0], fila[1]))

        consulta.close()
        conexion.close()

def ping_user(user):
        timeA = time()
        s.send("PRIVMSG %s :\x01PING %s\x01\n" % (user, timeA))

def hora_user():
        hora = datetime.datetime.now().hour - 12
        minutos = datetime.datetime.now().minute
        segundos = datetime.datetime.now().second
        print(hora, minutos, segundos)
        if minutos < 10:
                send_msg("son las %s:0%s:%s" % (abs(hora), minutos, segundos))
        else:
                send_msg("son las %s:%s:%s" % (abs(hora), minutos, segundos))
       

while 1:
        readbuffer=readbuffer+s.recv(1024)
        temp=string.split(readbuffer, "\n")
        readbuffer=temp.pop( )
        for line in temp:
                print(line)
                line=string.rstrip(line)
                line2=line.split(CHAN + " :")
                VarChannel = line2[0].split()
                username = line2[0].split('!')[0].split(':')[1]
                n = ''
                try:
                        CHAN_A = VarChannel[2]
                except IndexError:
                        CHAN_A = CHAN
                
                if line2[0].find("PING") != -1:
                        pingid = line2[0].split()[1]
                        s.send("PONG %s\r\n" % pingid)

                elif line2[0].find('JOIN') != -1:
                        if username != NICK and username.find(HOST) == -1:
                                try:
                                        user_ = line2[0].split("@")[0].split("~")[1]
                                except IndexError:
                                        try:
                                                user_ = line2[0].split("@")[0].split("!")[1]
                                        except IndexError:
                                                continue
                                host_user = VarChannel[0].split(":" +  NICK + "!" + "~" + user_)
                                host1 = host_user[0].split("@")
                                host2 = '*!*@' + host1[1]
                                
                                sleep(2)
                                send_msg("Bienvenid@ %s ^^\n" % username)


                def kick_user(user, razon=username):
                        s.send("KICK %s %s :%s\n" % (CHAN_A, user, razon))

                def invite_user(user, canal=CHAN_A):
                        s.send("INVITE %s %s\n" % (user, canal))

                def send_ban(user, chan=CHAN_A):
                        global readbuffer
                        if user.startswith('*!*'):
                                s.send("MODE %s +b %s\n" % (chan, user))
                        else:
                                s.send("WHOIS %s\n" % user)
                                sleep(0.1)
                                while 1:
                                        readbuffer=readbuffer+s.recv(1024)
                                        temp_=string.split(readbuffer, "\n")
                                        readbuffer=temp_.pop( )
                                        for line_ in temp_:
                                                line_=string.rstrip(line_)
                                                line_=line_.split()
                                                print(line_)
                                                if len(line_) > 1:
                                                        if line_[1] == '311':
                                                                host1 = line_[5]
                                                                host2 = "*!*@" + host1
                                                                s.send("MODE %s +b %s\n" % (chan, host2))
                                                                break
                                                        if line_[1] == '401':
                                                                s.send("PRIVMSG %s :Error: usuario no encontrado\n" % chan)
                                        break

                def send_unban(user, chan=CHAN_A):
                        global readbuffer
                        if user.startswith('*!*'):
                                s.send("MODE %s -b %s\n" % (chan, user))
                        else:
                                s.send("WHOIS %s\n" % user)
                                sleep(0.1)
                                while 1:
                                        readbuffer=readbuffer+s.recv(1024)
                                        temp_=string.split(readbuffer, "\n")
                                        readbuffer=temp_.pop( )
                                        for line_ in temp_:
                                                line_=string.rstrip(line_)
                                                line_=line_.split()
                                                print(line_)
                                                if len(line_) > 1:
                                                        if line_[1] == '311':
                                                                host1 = line_[5]
                                                                host2 = "*!*@" + host1
                                                                s.send("MODE %s -b %s\n" % (chan, host2))
                                                                break
                                                        if line_[1] == '401':
                                                                s.send("PRIVMSG %s :Error: usuario no encontrado\n" % chan)
                                        break

                #def send_ban_priv(chan, user):
                #        s.send("MODE %s +b %s\n" %s (chan, user))


                        
                if len(line2) > 1:


                                                
                        if 'DonaFlorinda' in line2[1].split():
                                send_msg("Vamos hijo, no te juntes con esta chusma\n")
                                sleep(2)
                                send_msg("Si mami. Chusma, chusma prfff\n")

                        if line2[1].find('http') != -1:
                                for u in line2[1].split():
                                        d = search('(.+://)(www.)?([^/]+)(.*)', u)
                                        if d:
                                                try:
                                                        raw = urlopen(u).read()
                                                        title = search('<title>([\w\W]+)</title>', raw).groups()[0]
                                                        title2 = ''
                                                        for t in title.split('\n'):
                                                                title2 += t.lstrip()+' '
                                                        send_msg("%s en %s\n" % (title2, d.groups()[2]))
                                                except AttributeError:
                                                        continue
                                                except IOError:
                                                        continue

                        if  line2[1] == '$sobre':
                                send_msg("a monton\n")

                        if  line2[1] == '*version' or line[1] == 'LinelBot, version' or line[1] == 'LinelBot version' or line[1] == 'LinelBot: version' :
                                send_msg("    __   _          _____       __ \n")
                                send_msg("   / /  (_)__  ___ / / _ )___  / /_\n")
                                send_msg("  / /__/ / _ \/ -_) / _  / _ \/ __/\n")
                                send_msg(" /____/_/_//_/\__/_/____/\___/\__/ \n")
                                send_msg("LinelBot v0.7 2017 \n")

                        if line2[1] == '*away':
                                if not username in away:
                                        send_msg("%s se marcha durante un tiempo. No molestar\n" % username)
                                        away.append(username)


                        if line2[1] == '*volvi' :
                                if username in away:
                                        send_msg("%s ha vuelto\n" % username)
                                        away.remove(username)

                        for l in line2[1].split():
                                if l in away != -1 and username != 'LinelBot':
                                        send_msg("no molestéis a %s que no esta, \n" % l)

                        if  line2[1] == 'Hola LinelBot' or line2[1] == 'hola LinelBot':
                                send_msg("Saludos a ti también %s\n" % username)
                        
                        if line2[1] == '*ping':
                                send_msg("Pong!\n")
                        
                        if line2[1] == 'achu' :
                                send_msg("salud!\n")
                        
                        if line2[1].startswith(NICK) or line2[1].startswith(NICK + ",") or line2[1].startswith(NICK + ":"):
                                linea = line2[1].split()
                                try:
                                        parametro2 = linea[1]
                                except IndexError:
                                        parametro2 = None
                                if parametro2 == None:
                                        send_msg('Comandos-->*help \n')
              
                        if "#" in line2[1]:
                                linea1_ = line2[0].split()
                                if linea1_[1] == "PRIVMSG":
                                        if check_user(username) == False:
                                                if not username in user_fail:
                                                        if not "#" + " " in line2[1]:
                                                                kick_user(username, "Esta prohibido el spam en este canal")
                                                                user_fail.append(username)
                                                else:
                                                        try:
                                                                user_ = line2[0].split("@")[0].split("~")[1]
                                                        except IndexError:
                                                                user_ = line2[0].split("@")[0].split("!")[1]
                                                        host_user = VarChannel[0].split(":" +  NICK + "!" + "~" + user_)
                                                        print(user_)
                                                        print(host_user)
                        
                                                        host1 = host_user[0].split("@")
                                                        print(host1)
                                                        host2 = '*!*@' + host1[1]
                                                        print(host2)
                        
                                                        s.send("MODE %s +b %s\n" % (CHAN_A, host2))
                                                        kick_user(username, "Esta prohibido el spam en este canal")
                
                        if line2[1].startswith("*join"):
                                send_msg("Comando en privado")
                                #linea = line2[1].split()
                                #try:
                                #       CHA = linea[1]
                                #except IndexError:
                                #       CHA = None
                                #if CHA == None:
                                #       send_msg("Por favor coloque el canal a entrar ej:\"*join (canal)\"")
                                #if not CHA.startswith("#"):
                                #       send_msg("Canal Invalido.")
                                #else:
                                #       print CHA
                                #       send_join(CHA)
                         
                        if line2[1] == '*help' :
                                if check_user(username) == False:
                                        send_notice(username, 'Comandos para usuario estandar')
                                        send_notice(username, '*version')
                                        sleep(0.50)
                                        send_notice(username, '*away')
                                        send_notice(username, '*volvi')
                                        sleep(0.50)
                                        send_notice(username, '*ping')
                                        send_notice(username, '*moneda')
                                        
                                if check_user(username) == True:
                                        send_notice(username, 'Comandos para usuarios con permisos de OP')
                                        send_notice(username, '*version')
                                        sleep(0.50)
                                        send_notice(username, '*away')
                                        send_notice(username, '*volvi')
                                        send_notice(username, '*ping')
                                        sleep(0.50)
                                        send_notice(username, '*moneda')
                                        send_notice(username, '*join')
                                        send_notice(username, '*op')
                                        sleep(0.50)
                                        send_notice(username, '*deop')
                                        send_notice(username, '*kick')

                        if line2[1] == '*logout' :
                                send_priv('logout\n')
                        
                        if line2[1] == '*' + '' or line2[1] == '**' or line2[1] == "*" + str():
                                send_msg('error comando desconocido\n')
                        
                        if "*op" in line2[1] or "LinelBot op" in line2[1] or "LinelBot, op" in line2[1] or "LinelBot: op" in line2[1]:
                                linea = line2[1].split()
                                try:
                                        user_op = linea[1]
                                        print(user_op)
                                except  IndexError:
                                        user_op = None

                                if check_user(username) == False:
                                        send_msg("Permisos Insuficientes.")
        
                                if check_user(username) == True:
                                        
                                                if user_op == "op":
                                                        try:
                                                                user_op = linea[2]
                                                        except IndexError:
                                                                user_op = None
                                                if user_op == None:
                                                        send_mode_op(username)
                                                if user_op != None:
                                                        long_ = len(user_op)
                                                        user_op = " ".join(linea[1:])
                                                        send_mode_op(user_op)
                        if line2[1].startswith("*deop") or line2[1].startswith("*dp") or line2[1].startswith(NICK + " deop") or line2[1].startswith(NICK + ", deop") or line2[1].startswith(NICK + ": deop"):
                                linea = line2[1].split()
                                try:
                                        user = linea[1]
                                except IndexError:
                                        user = None
                                
                                if check_user(username) == False:
                                        send_msg("Error: Permisos Insuficientes.")

                                if check_user(username) == True:
                                                if user == "deop":
                                                        try:
                                                                user = linea[2]
                                                        except IndexError:
                                                                user = None
                                                if user == None:
                                                        send_mode_deop(username)
                                                if user != None:
                                                        send_mode_deop(user)

                        if line2[1].startswith("*register"):
                                #send_msg('Registro Deshabilítado.')
                                linea = line2[1].split()
                                try:
                                        user = linea[1]
                                except IndexError:
                                        user = None
                                if user == None:
                                        register_user(username)
                                elif user != None:
                                        if check_user(username) == True:
                                                register_user(user)
                                        elif check_user(username) == False:
                                                send_msg("Permisos Insuficientes.")

                        
                        if line2[1].startswith("*kick"):
                                linea = line2[1].split()
                                try:
                                        user = linea[1]
                                except IndexError:
                                        user = None
                                try:
                                        razon = linea[2:]
                                except IndexError:
                                        razon = None
                                if check_user(username) == False:
                                        send_msg("Permisos Insuficientes")
                                elif user == None:
                                        send_msg("No se me a pasado ningún usuario")
                                        
                                elif check_user(username) == True:

                                        if user == NICK:
                                                send_msg("No es gracioso")
                                        elif razon == None:
                                                kick_user(user)
                                        elif razon != None:
                                                razon = " ".join(razon)
                                                kick_user(user, razon)

                        if line2[1].startswith("*invite"):
                                linea = line2[1].split()
                                try:
                                        user = linea[1]
                                except IndexError:
                                        user = None
                                try:
                                        canal = linea[2]
                                except IndexError:
                                        canal = None
                                if user == None:
                                        send_msg("Error: no se me a pasado el usuario")
                                if canal == None:
                                        invite_user(user)
                                else:
                                        invite_user(user, canal)

                        if line2[1] == "*list op":
                                list_op()

                        if line2[1] == "*list all":
                                list_all()
                                
                        if line2[1].startswith("*part"):
                                linea = line2[1].split()
                                try:
                                        chann = linea[1]
                                except IndexError:
                                        chann = None
                                if chann == None:
                                        send_part(CHAN_A)
                                elif chann != None:
                                        send_part(chann)
                        
                        if line2[1] == "*moneda":
                                moneda()

                        if line2[1].startswith("*add op"):
                                linea = line2[1].split()
                                try:
                                        user = linea[2]
                                except IndexError:
                                        user = None

                                if username != FOUNDER:
                                        send_msg("Permisos Insuficientes.")
                                
                                elif user == None:
                                        send_msg("Error: no se a pasado ningún usuario.")
                                elif username == FOUNDER:
                                        set_permisos_op(user)

                        if line2[1].startswith("*drop op"):
                                linea = line2[1].split()
                                try:
                                        user = linea[2]
                                except IndexError:
                                        user = None

                                if username != FOUNDER:
                                        send_msg("Permisos Insuficientes.")
                                
                                elif user == None:
                                        send_msg("Error: no se a pasado ningún usuario.")
                                elif username == FOUNDER:
                                        drop_permisos_op(user)       
                                        
                        if line2[1].startswith("*add voice"):
                                linea = line2[1].split()
                                try:
                                        user = linea[2]
                                except IndexError:
                                        user = None

                                if username != FOUNDER:
                                        send_msg("Permisos Insuficientes.")

                                elif user == None:
                                        send_msg("Error: no se a pasado ningún usuario.")
                                elif username == FOUNDER:
                                        set_permisos_voice(user)

                        if line2[1].startswith("*drop voice"):
                                linea = line2[1].split()
                                try:
                                        user = linea[2]
                                except IndexError:
                                        user = None

                                if username != FOUNDER:
                                        send_msg("Permisos Insuficientes.")

                                elif user == None:
                                        send_msg("Error: no se a pasado ningún usuario.")
                                elif username == FOUNDER:
                                        drop_permisos_voice(user)
                        if line2[1].startswith("*voice") or line2[1].startswith("*v") or line2[1].startswith("LinelBot, v") or line2[1].startswith("LinelBot: v") or line2[1].startswith("LinelBot v") or line2[1].startswith("LinelBot, voice") or line2[1].startswith("LinelBot: voice") or line2[1].startswith("LinelBot voice"):
                                if line2[1] == "*v":
                                        linea = line2[1].split()
                                        try:
                                                user = linea[1]
                                        except IndexError:
                                                user = None

                                        if check_user_voice(username) == False:
                                                        send_msg("Permisos Insuficientes.")

                                        if check_user_voice(username) == True:
                                                if user == "voice":
                                                        try:
                                                                user = linea[2]
                                                        except IndexError:
                                                                user = None
                                                if user == None:
                                                        send_mode_voice(username)
                                                elif user != None:
                                                        send_mode_voice(user)

                        if line2[1].startswith("*dv") or line2[1].startswith("*devoice") or line2[1].startswith("LinelBot, dv") or line2[1].startswith("LinelBot: dv") or line2[1].startswith("LinelBot dv") or line2[1].startswith("LinelBot, devoice") or line2[1].startswith("LinelBot: devoice") or line2[1].startswith("LinelBot devoice"):
                                if line2[1] == "*dv":
                                        linea = line2[1].split()
                                        try:
                                                user = linea[1]
                                        except IndexError:
                                                user = None

                                        if check_user(username) == False:
                                                if check_user_voice == False:
                                                        send_msg("Permisos Insuficientes.")

                                        if check_user_voice(username) == True:
                                                if user == "devoice":
                                                        try:
                                                                user = linea[2]
                                                        except IndexError:
                                                                user = None
                                                if user == None:
                                                        send_mode_devoice(username)
                                                elif user != None:
                                                        send_mode_devoice(user)

                        if line2[1].startswith("*ban"):
                                linea = line2[1].split()
                                try:
                                        user = linea[1]
                                except IndexError:
                                        user = None
                                if user != None:
                                        send_ban(user)

                        if line2[1].startswith("*hola"):
                                send_msg("hola %s" % username)

                        if line2[1].startswith("*unban"):
                                linea = line2[1].split()
                                try:
                                        user = linea[1]
                                except IndexError:
                                        user = None
                                if user != None:
                                        send_unban(user)

                        if line2[1].startswith("*lag"):
                                ping_user(username)

                        if line2[1].startswith("*hora"):
                                hora_user()
                                
                        if line2[1].startswith("*verify"):
                                if not line2[1] == "*v":
                                        user = line2[1].split()[1]
                                        user_account(user)
        
                if len(line) >= 3:
                        linea = line
                        linea2 = linea.split(CHAN_A + " :")
                        #print(linea2)

                        
                        if len(linea2) > 1:
                                if CHAN_A != CHAN:
                                                        
                                        if linea2[1] == '*ping':
                                                send_msg("Pong!")

                                                
                                        if "*op" in linea2[1] or "LinelBot op" in linea2[1] or "LinelBot: deop" in linea2[1] or "LinelBot, op" in linea2[1]:
                                                print(linea)
                                                linea1 = linea2[1].split()
                                                try:
                                                        user_op = linea1[1]
                                                        print(user_op)
                                                except  IndexError:
                                                        user_op = None

                                                if check_user(username) == False:
                                                        send_msg("Permisos Insuficientes.")

                                                if check_user(username) == True:
                                                        if user_op == "op":
                                                                try:
                                                                        user_op = linea2[5]
                                                                except IndexError:
                                                                        user_op = None
                                                        if user_op == None:
                                                                long_ = 1
                                                                send_mode_op(username)
                                                        if user_op != None:
                                                                long_ = len(user_op)
                                                                user_op = " ".join(linea[1:])
                                                                send_mode_op(user_op)
                                                
                                        if "*deop" in linea2[1] or NICK + " deop" in linea2[1] or NICK + ", deop" in linea2[1] or NICK + ": deop" in linea2[1]:
                                                        linea1 = linea2[1].split()
                                                        try:
                                                                user = linea1[1]
                                                        except IndexError:
                                                                user = None

                                                        if check_user(username) == False:
                                                                send_msg("Permisos Insuficientes.")

                                                        if check_user(username) == True:
                                                                if user == "deop":
                                                                        try:
                                                                                user = linea1[2]
                                                                        except IndexError:
                                                                                user = None
                                                                if user == None:
                                                                        send_mode_deop(username)
                                                                if user != None:
                                                                        long_ = len(user)
                                                                        user = " ".join(linea[1:])
                                                                        send_mode_deop(user)
                                                
                                                
                                        if linea2[1].startswith("*invite"):
                                                linea1 = linea2[1].split()
                                                try:
                                                        user = linea1[1]
                                                except IndexError:
                                                        user = None
                                                try:
                                                        canal = linea1[2]
                                                except IndexError:
                                                        canal = None
                                                if user == None:
                                                        send_msg("Error: no se me a pasado el usuario")
                                                if canal == None:
                                                        invite_user(user)
                                                else:
                                                        invite_user(user, canal)

                                        if linea2[1].startswith("*kick") or linea2[1].startswith("*k"):
                                                linea1 = linea2[1].split()
                                                try:
                                                        user = linea1[1]
                                                except IndexError:
                                                        user = None
                                                try:
                                                        razon = linea1[2:]
                                                except IndexError:
                                                        razon = None
                                                if check_user(username) == False:
                                                        send_msg("Error: Permisos Insuficientes")
                                                if user == None:
                                                        send_msg("Error: No se me a pasado ningún usuario")
                                                        
                                                if check_user(username) == True or check_user_voice == True:

                                                        if user == "kick":
                                                                try:
                                                                        user = linea1[2]
                                                                except IndexError:
                                                                        user = None
                                                        if user == NICK:
                                                                send_msg("No es gracioso")
                                                        if razon == None:
                                                                kick_user(user)
                                                        elif razon != None:
                                                                razon = " ".join(razon)
                                                                kick_user(user, razon)

                                        if linea2[1].startswith("*list op"):
                                                list_op()

                                        if linea2[1].startswith("*add op"):
                                                linea1 = linea2[1].split()
                                                try:
                                                        user = linea1[2]

                                                except IndexError:
                                                        user = None
                                                if username != FOUNDER:
                                                        send_msg("Permisos Insuficientes")
                                                elif username == FOUNDER:
                                                        if user == None:
                                                                send_msg("No se ha pasado ningun usuario")
                                                        else:
                                                                print(user)
                                                                set_permisos_op(user)
                                        if linea2[1].find('http') != -1:
                                                try:
                                                        for u in linea2[1].split():
                                                                d = search('(.+://)(www.)?([^/]+)(.*)', u)
                                                                if d:
                                                                        raw = urlopen(u).read()
                                                                        title = search('<title>([\w\W]+)</title>', raw).groups()[0]
                                                                        title2 = ''
                                                                        for t in title.split('\n'):
                                                                                title2 += t.lstrip()+' '
                                                                        send_msg("%s en %s\n" % (title2, d.groups()[2]))
                                                except IOError:
                                                        continue
                                                except AttributeError:
                                                        continue
                                        if linea2[1].startswith("*lag"):
                                                ping_user(username)

                                        if linea2[1].startswith("*part"):
                                                linea = linea2[1].split()
                                                try:
                                                        chann = linea[1]
                                                except IndexError:
                                                        chann = None
                                                if chann == None:
                                                        send_part(CHAN_A)
                                                elif chann != None:
                                                        send_part(chann)

                                        if "#"  in linea2[1]:
                                                if not linea2[1].startswith("*join"):
                                                        if check_user(username) == False:
                                                                if not username in user_fail:
                                                                        if not "#" + " " in linea2[1]:
                                                                                kick_user(username, "Esta prohibido el spam en este canal")
                                                                                user_fail.append(username)
                                                                else:
                                                                        try:
                                                                                user_ = linea2[0].split("@")[0].split("!")[0]
                                                                        except IndexError:
                                                                                user_ = linea2[0].split("@")[0].split("~")[0]
                                                                        host_user = VarChannel[0].split(":" +  NICK + "!" + "~" + user_)
                                                                        print(user_)
                                                                        print(host_user)
                
                                                                        host1 = host_user[0].split("@")
                                                                        try:
                                                                                host2 = '*!*@' + host1[1]
                                                                        except IndexError:
                                                                                continue
                
                                                                        s.send("MODE %s +b %s\n" % (CHAN_A, host2))
                                                                        kick_user(username, "Esta prohibido el spam en este canal")

                                        if linea2[1] == '*help' :
                                                if check_user(username) == False:
                                                        send_notice(username, 'Comandos para usuario estandar')
                                                        send_notice(username, '*version')
                                                        sleep(0.50)
                                                        send_notice(username, '*away')
                                                        send_notice(username, '*volvi')
                                                        sleep(0.50)
                                                        send_notice(username, '*ping')
                                                        send_notice(username, '*moneda')
                                        
                                                if check_user(username) == True:
                                                        send_notice(username, 'Comandos para usuarios con permisos de OP')
                                                        send_notice(username, '*version')
                                                        sleep(0.50)
                                                        send_notice(username, '*away')
                                                        send_notice(username, '*volvi')
                                                        send_notice(username, '*ping')
                                                        sleep(0.50)
                                                        send_notice(username, '*moneda')
                                                        send_notice(username, '*join')
                                                        send_notice(username, '*op')
                                                        sleep(0.50)
                                                        send_notice(username, '*deop')
                                                        send_notice(username, '*kick')

                                        if "*voice" in linea2[1] or "*v" in linea2[1] or "LinelBot, v" in linea2[1] or "LinelBot: v" in linea2[1] or "LinelBot v" in linea2[1] or "LinelBot, voice" in linea2[1] or "LinelBot: voice" in linea2[1] or "LinelBot voice" in linea2[1]:
                                                linea = linea2[1].split()
                                                try:
                                                        user = linea[1]
                                                except IndexError:
                                                        user = None

                                                if check_user_voice(username) == False:
                                                                send_msg("Permisos Insuficientes.")

                                                if check_user_voice(username) == True:
                                                        if user == "voice":
                                                                try:
                                                                        user = linea[2]
                                                                except IndexError:
                                                                        user = None
                                                        if user == None:
                                                                send_mode_voice(username)
                                                        if user != None:
                                                                send_mode_voice(user)
                                        if "*dv" in linea2[1] or "*devoice" in linea2[1] or "LinelBot, dv" in linea2[1] or "LinelBot: dv" in linea2[1] or "LinelBot dv" in linea2[1] or "LinelBot, devoice" in linea2[1] or "LinelBot: devoice" in linea2[1] or "LinelBot devoice" in linea2[1]:
                                                linea = linea2[1].split()
                                                try:
                                                        user = linea[1]
                                                except IndexError:
                                                        user = None

                                                if check_user(username) == False:
                                                        if check_user_voice == False:
                                                                send_msg("Permisos Insuficientes.")

                                                if check_user(username) == True or check_user_voice(username) == True:
                                                        if user == "devoice":
                                                                try:
                                                                        user = linea[2]
                                                                except IndexError:
                                                                        user = None
                                                        if user == None:
                                                                send_mode_devoice(username)
                                                        if user != None:
                                                                send_mode_devoice(user)
                                
                if line[0].find("PRIVMSG " + NICK):
                        linea_ = line
                        linea_ = linea_.split("PRIVMSG " + NICK + " :")
                        

                        if len(linea_) > 1:

                                if linea_[1].startswith("join"):
                                        linea_1 = linea_[1].split()
                                        try:
                                                chann = linea_1[1]
                                        except IndexError:
                                                chann = None

                                        if username != FOUNDER:
                                                send_priv(username, "Permisos Insuficientes")

                                        elif chann == None:
                                                send_priv(username, "No se ha pasado un canal")
                                        elif not chann.startswith("#"):
                                                send_priv(username, "Canal invalido")

                                        elif username == FOUNDER:
                                                send_join(chann)
                                if linea_[1].startswith("msg"):
                                        linea_1 = linea_[1].split()
                                        try:
                                                chann = linea_1[1]
                                        except IndexError:
                                                chann = None
                                        try:
                                                msg = linea_1[2:]
                                        except IndexError:
                                                msg = None

                                        if check_user(username) == False:
                                                send_priv(username, "Permisos insuficientes")

                                        elif chann != None and msg != None:
                                                msg = " ".join(msg)
                                                send_priv(chann, msg)
                if line[0].find("NOTICE " + NICK):
                        lineal = line
                        lineal = lineal.split("NOTICE " + NICK + " :")

                        if len(lineal) > 1:
                                if lineal[1].startswith("\x01PING"):
                                        lineal1 = lineal[1].split()
                                        ping = lineal1[1].split("\x01")
                                        lag = time() - float(ping[0])
                                        send_notice(username, "lag : "+ str(round(lag, 2)) + "s")
                                                        
                        

# syslogKeyextractor

`syslogKeyextractor` es un script en Python diseñado para analizar archivos de syslog con formato "key:value" para identificar el nombre de cada "key" y que "tipo de dato" es la parte "value", genera un archivo CSV con la información extraída, proporcionando una vista clara de los tipos de datos presentes en el syslog.

## Requisitos

- Python 3.x

## Instalación

1. Clona el repositorio o descarga el script `keyextractor.py` en tu máquina local.

    ```sh
    git clone https://github.com/k0jir0900/syslogKeyextractor.git 
    cd syslogKeyextractor
    ```

## Uso

Ejecuta el script desde la línea de comandos proporcionando los parámetros necesarios.

### Parámetros

- `-f`, `--file` (obligatorio): Ruta al archivo de syslog que deseas analizar.
- `-ks`, `--key_separator` (opcional): Separador para las llaves. Por defecto es un espacio (` `).
- `-kv`, `--kv_separator` (opcional): Separador para los pares key:value. Por defecto es el signo igual (`=`).
- `-o`, `--output` (opcional): Nombre del archivo CSV de salida. Por defecto es `eventKey_sample.csv`.

### Ejemplo de uso 1: Uso por defecto.

Los valores por defecto son:

- Como separador de llaves ` `
- Como separador key:value `=`
- El archivo output tendrá nombre `eventKey_sample.csv`
- Se debe indicar la ruta del archivo con la muestras utilizando el flag `-f`

1. Crear archivo con ejemplos de log a analizar. Este archivo debe estar en formato `EventName`,`SyslogSample`.

```plaintext
Unauthorized Access Attempt(40020),0|Palo AltoNetworks|PAN-OS|10.2.5|Unauthorized Access Attempt(40020)|THREAT|4|rt=Mar 21 2021 11:22:45 GMTdeviceExternalId=987654321 src=10.10.10.10 dst=10.20.20.20 sourceTranslatedAddress=1.1.1.1destinationTranslatedAddress=2.2.2.2 cs1Label=Rule cs1=Azure suser=userA duser=userB app=sshcs3Label=Virtual System cs3=vsys1 cs4Label=Source Zone cs4=Internal cs5Label=Destination Zone cs5=ExternaldeviceInboundInterface=eth0 deviceOutboundInterface=eth1 cs6Label=LogProfile cs6=Log_Standardcn1Label=SessionID cn1=9876543 cnt=2 spt=10234 dpt=2222 sourceTranslatedPort=1111destinationTranslatedPort=2222 flexString1Label=Flags flexString1=0x80002401 proto=udp act=allowrequest= cs2Label=URL Category cs2=finance flexString2Label=Direction flexString2=server-to-clientPanOSActionFlags=0x1 externalId=1234567890123456789 cat=vulnerability fileId=2345678901234567890 PanOSDGl1=1PanOSDGl7=1 PanOSDGl4=1 PanOSDGl4=1PanOSVsysName=VSYS-Finance dvchost=FW-PAN-02 PanOSSrcUUID=uuid1 PanOSDstUUID=uuid2PanOSTunnelID=1 PanOSMonitorTag= PanOSParentSessionID=1PanOSParentStartTime=PanOSTunnelType=N/APanOSThreatCategory=unauthorized-access PanOSContentVer=AppThreat-9999-9999 PanOSAssocID=1 PanOSPPID=4294967296 PanOSHTTPHeader=PanOSURLCatList= PanOSRuleUUID=abcd1234-5678-90ef-ghij-klmn12345678 PanOSHTTP2Con=1PanDynamicUsrgrp=PanXFFIP=PanSrcDeviceCat=PanSrcDeviceProf=PanSrcDeviceModel= PanSrcDeviceVendor=PanSrcDeviceOS=PanSrcDeviceOSv= PanSrcHostname=PanSrcMac=PanDstDeviceCat=PanDstDeviceProf=PanDstDeviceModel=PanDstDeviceVendor=
Malicious Login Attempt(40021),0|Palo AltoNetworks|PAN-OS|10.2.5|Malicious Login Attempt(40021)|THREAT|4|rt=Aug 14 2022 09:15:55 GMTdeviceExternalId=234567890 src=192.168.1.1 dst=192.168.1.2 sourceTranslatedAddress=3.3.3.3destinationTranslatedAddress=4.4.4.4 cs1Label=Rule cs1=GCP suser=userC duser=userD app=sshcs3Label=Virtual System cs3=vsys2 cs4Label=Source Zone cs4=DMZ cs5Label=Destination Zone cs5=SecuredeviceInboundInterface=eth2 deviceOutboundInterface=eth3 cs6Label=LogProfile cs6=Log_High_Securitycn1Label=SessionID cn1=1234567 cnt=3 spt=20234 dpt=3333 sourceTranslatedPort=4444destinationTranslatedPort=5555 flexString1Label=Flags flexString1=0x80002402 proto=icmp act=blockrequest= cs2Label=URL Category cs2=education flexString2Label=Direction flexString2=server-to-clientPanOSActionFlags=0x2 externalId=9876543210987654321 cat=vulnerability fileId=3456789012345678901 PanOSDGl1=2PanOSDGl7=2 PanOSDGl4=2 PanOSDGl4=2PanOSVsysName=VSYS-Secure dvchost=FW-PAN-03 PanOSSrcUUID=uuid3 PanOSDstUUID=uuid4PanOSTunnelID=2 PanOSMonitorTag=PanOSParentSessionID=2PanOSParentStartTime=PanOSTunnelType=N/APanOSThreatCategory=malicious-login PanOSContentVer=AppThreat-7777-8888 PanOSAssocID=2 PanOSPPID=4294967297 PanOSHTTPHeader=PanOSURLCatList=PanOSRuleUUID=dcba4321-8765-09fe-hijk-lmn6543210 PanOSHTTP2Con=2PanDynamicUsrgrp=PanXFFIP=PanSrcDeviceCat=PanSrcDeviceProf=PanSrcDeviceModel=PanSrcDeviceVendor=PanSrcDeviceOS=PanSrcDeviceOSv=PanSrcHostname=PanSrcMac=PanDstDeviceCat=PanDstDeviceProf=PanDstDeviceModel=PanDstDeviceVendor=
```
2. Ejecuta el script indicando el nombre del archivo creado en el paso 1, en este caso `sample.txt` 

```sh
python keyextractor.py -f sample.txt
```

3. Si no se definio otro nombre con el flag `-o`, se generara el archivo `eventKey_sample.csv` con el siguiente formato:

- El nombre de la columna será el nombre del evento
- En las filas debajo de cada evento se visualizará en formato `key`:`DataType` con la información extraida.


| Unauthorized Access Attempt(40020)  | Malicious Login Attempt(40021)      |
|-------------------------------------|-------------------------------------|
| src:string       | src:string |
| dst:string       | dst:string   |
| sourceTranslatedAddress:string      | sourceTranslatedAddress:string |
| cs1Label:string     | cs1Label:string   |

### Ejemplo de uso 2: Utilizando separadores de "key" custom.

En este ejemplo el syslog tiene como separador "|" y utilizaremos el flag "-ks" para definir un separador de "key" custom.

1. Crear archivo con ejemplos de log a analizar. Este archivo debe estar en formato `EventName`,`SyslogSample`.

```plaintext
Access Granted,apr. 15 10:45:22|Remote Access|Session Control|16.x+|520|Access Granted|deviceHost=pra2|sessionId=f6a231b1234c4ab5986ac2ab435d7890|externalKeyLabel=Auth Key|jumpGroupId=45|jumpGroupName=Tech_Support|jumpGroupType=shared|dstUser=TechUser1|dstUid=1.14.115.140|
Login Attempt,may. 10 08:20:45|Remote Access|Security Event|16.x+|505|Login Attempt|deviceHost=pra3|sessionId=d8e412d9876f4dc2345bd6e2ab983c10|externalKeyLabel=Auth Key|jumpGroupId=72|jumpGroupName=Admin_Access|jumpGroupType=shared|dstUser=AdminUser2|dstUid=1.15.117.150|
```

2. Ejecuta el script indicando el nombre del archivo creado en el paso 1, en este caso `sample.txt` 

```sh
python keyextractor.py -f sample.txt -ks "|"
```

3. Si no se definio otro nombre con el flag `-o`, se generara el archivo `eventKey_sample.csv` con el siguiente formato:

- El nombre de la columna será el nombre del evento
- En las filas debajo de cada evento se visualizará en formato `key`:`DataType` con la información extraida.


| Access Granted  | Login Attempt  |
|-----------------|----------------|
| deviceHost:string  | deviceHost:string |
| sessionId:string   | sessionId:string   |
| externalKeyLabel:string  | externalKeyLabel:string |
| jumpGroupId:int  | jumpGroupId:int  |

# Bonus
```sh
| summarize s = make_set(SyslogMessageV3) by DeviceEventClassID
| extend l = s[0]
| project DeviceEventClassID, l
```

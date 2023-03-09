import re 
text = '''EMIRATOS ÁRABES UNIDOS	Dirham DE EAU	AED	784
AFGANISTÁN	Afgani afgano	AFN	971
ALBANIA	Lek	ALL	008
ARMENIA	Dram armenio	AMD	051
CURAZAO	Florín antillano neerlandés	ANG	532
SAN MARTÍN (PARTE HOLANDESA)	Florín holandés	ANG	532
ANGOLA	Kwanza angoleño	AOA	973
ARGENTINA	Peso argentino	ARS	032
AUSTRALIA	Dólar australiano	AUD	036
ISLA DE NAVIDAD	Dólar australiano	AUD	036
ISLAS COCOS (KEELING)	Dólar australiano	AUD	036
ISLAS HEARD Y McDONALD	Dólar australiano	AUD	036
KIRIBATI	Dólar australiano	AUD	036
NAURU	Dólar australiano	AUD	036
ISLA NORFOLK	Dólar australiano	AUD	036
TUVALU	Dólar tuvaluano	AUD	036
ARUBA	Florín arubeño	AWG	533
AZERBAIYÁN	Manat azerbaiyano	AZN	944
BOSNIA Y HERZEGOVINA	Marco bosnioherzegovino	BAM	977
BARBADOS	Dólar de Barbados	BBD	052
BANGLADESH	Taka	BDT	050
BULGARIA	Lev	BGN	975
BARÉIN	Dinar bareiní	BHD	048
BURUNDI	Franco burundés	BIF	108
BERMUDA	Dólar bermudeño	BMD	060
BRUNÉI DARUSSALAM	Dólar de Brunei	BND	096
BOLIVIA (ESTADO PLURINACIONAL DE)	Boliviano	BOB	068
BOLIVIA (ESTADO PLURINACIONAL DE)	Mvdol	BOV	984
BRASIL	Real brasileño	BRL	986
BAHAMAS (LAS)	Dólar bahameño	BSD	044
BUTÁN	Ngultrum butanés	BTN	064
BOTSUANA	Pula	BWP	072
BIELORRUSIA	Rublo bielorruso	BYR	974
BELICE	Dólar beliceño	BZD	084
CANADÁ	Dólar canadiense	CAD	124
CONGO (REPÚBLICA DEMOCRÁTIC DEL)	Franco congoleño	CDF	976
SUIZA	WIR Euro	CHE	947
LIECHTENSTEIN	Franco suizo	CHF	756
SUIZA	Franco suizo	CHF	756
SUIZA	Franco WIR	CHW	948
CHILE	Unidad de Fomento	CLF	990
CHILE	Peso chileno	CLP	152
CHINA	Renminbi	CNY	156
COLOMBIA	Peso colombiano	COP	170
COLOMBIA	Unidad de valor real	COU	970
COSTA RICA	Colón costarricense	CRC	188
CUBA	Peso convertible	CUC	931
CUBA	Peso cubano	CUP	192
CABO VERDE	Escudo caboverdiano	CVE	132
REPÚBLICA CHECA	Czech Koruna	CZK	203
YIBUTI	Franco yibutiano	DJF	262
DINAMARCA	Corona danesa	DKK	208
ISLAS FAROE	Corona danesa	DKK	208
GROENLANDIA	Corona danesa	DKK	208
REPÚBLICA DOMINICANA	Peso dominicano	DOP	214
ALGERIA	Dinar argelino	DZD	012
EGIPTO	Libra egipcia	EGP	818
ERITREA	Nakfa	ERN	232
ETIOPÍA	Birr etíope	ETB	230
ISLAS ÅLAND	Euro	EUR	978
ANDORRA	Euro	EUR	978
AUSTRIA	Euro	EUR	978
BÉLGICA	Euro	EUR	978
CHIPRE	Euro	EUR	978
ESTONIA	Euro	EUR	978
UNIÓN EUROPEA	Euro	EUR	978
FINLANDIA	Euro	EUR	978
FRANCIA	Euro	EUR	978
GUYANA FRANCESA	Euro	EUR	978
TERRITORIOS AUSTRALES FRANCESES	Euro	EUR	978
ALEMANIA	Euro	EUR	978
GRECIA	Euro	EUR	978
GUADALUPE	Euro	EUR	978
SANTA SEDE	Euro	EUR	978
IRLANDA	Euro	EUR	978
ITALIA	Euro	EUR	978
LETONIA	Euro	EUR	978
LITUANIA	Euro	EUR	978
LUXEMBURGO	Euro	EUR	978
MALTA	Euro	EUR	978
MARTINICA	Euro	EUR	978
MAYOTTE	Euro	EUR	978
MÓNACO	Euro	EUR	978
MONTENEGRO	Euro	EUR	978
HOLANDA	Euro	EUR	978
PORTUGAL	Euro	EUR	978
REUNIÓN	Euro	EUR	978
SAN BARTOLOMÉ	Euro	EUR	978
SAN MARTÍN	Euro	EUR	978
SAN PEDRO Y MIQUELÓN	Euro	EUR	978
SAN MARINO	Euro	EUR	978
ESLOVAQUIA	Euro	EUR	978
ESLOVENIA	Euro	EUR	978
ESPAÑA	Euro	EUR	978
FIJI	Dólar fiyiano	FJD	242
ISLAS MALVINAS	Libra malvinense	FKP	238
GUERNSEY	Libra esterlina	GBP	826
ISLA DE MAN	Libra esterlina	GBP	826
JERSEY	Libra esterlina	GBP	826
REINO UNIDO DE GRAN BRETAÑA E IRLANDA DEL NORTE	Libra esterlina	GBP	826
GEORGIA	Lari	GEL	981
GHANA	Cedi	GHS	936
GIBRALTAR	Libra gibraltareña	GIP	292
GAMBIA	Dalasi	GMD	270
GUINEA	Franco guineano	GNF	324
GUATEMALA	Quetzal	GTQ	320
GUYANA	Dólar guyanés	GYD	328
HONG KONG	Dólar de Hong Kong	HKD	344
HONDURAS	Lempira	HNL	340
CROACIA	Kuna	HRK	191
HAITÍ	Gourde	HTG	332
HUNGRÍA	Forinto húngaro	HUF	348
INDONESIA	Rupia indonesia	IDR	360
ISRAEL	Nuevo séquel	ILS	376
BUTÁN	Rupia india	INR	356
INDIA	Rupia india	INR	356
IRAK	Dinar iraquí	IQD	368
REPÚBLICA ISLAMICA DE IRÁN	Rial iraní	IRR	364
ISLANDIA	Corona islandesa	ISK	352
JAMAICA	Dólar jamaiquino	JMD	388
JORDANIA	Dinar jordano	JOD	400
JAPÓN	Yen	JPY	392
KENIA	Chelín keniano	KES	404
KIRGUISTÁN	Som	KGS	417
CAMBOYA	Riel camboyano	KHR	116
COMORAS	Franco comorense	KMF	174
REPÚBLICA DEMOCRATICA DE COREA DEL NORTE	Won norcoreano	KPW	408
REPÚBLICA DE COREA DEL SUR	Won	KRW	410
KUWAIT	Dinar kuwaití	KWD	414
ISLAS CAIMÁN (LAS)	Dólar de las Islas Cayman	KYD	136
KAZAJISTÁN	Tenge kazajo	KZT	398
REPUBLICA DEMOCRÁTICA POPULAR LAO	Kip laosiano	LAK	418
LÍBANO	Libra libanesa	LBP	422
SRI LANKA	Rupia de Sri Lanka	LKR	144
LIBERIA	Dólar liberiano	LRD	430
LESOTO	Loti	LSL	426
LIBIA	Dinar libio	LYD	434
MARRUECOS	Dírham marroquí	MAD	504
SAHARA OCCIDENTAL	Dirham marroquí	MAD	504
REPÚBLICA DE MOLDAVIA	Leu Moldavo	MDL	498
MADAGASCAR	Ariary malgache	MGA	969
MACEDONIA	Dinar	MKD	807
BIRMANIA	Kyat birmano	MMK	104
MONGOLIA	Tugrik	MNT	496
MACAO	Pataca	MOP	446
MAURITANIA	Uguiya	MRO	478
MAURICIO	Rupia de Mauricio	MUR	480
MALDIVAS	Rupia de maldivas	MVR	462
MALAWI	Kwacha malauí	MWK	454
MÉXICO	Peso mexicano	MXN	484
MÉXICO	Unidad de Inversion Mexicana(UDI)	MXV	979
MALASIA	Ringgit malayo	MYR	458
MOZAMBIQUE	Metical mozambiqueño	MZN	943
NAMIBIA	Dólar de Namibia	NAD	516
NIGERIA	Naira	NGN	566
NICARAGUA	Córdoba oro	NIO	558
ISLA BOUVET	Corona noruega	NOK	578
NORUEGA	Corona noruega	NOK	578
ISLAS SVALBARD Y JAN MAYEN	Corona noruega	NOK	578
NEPAL	Rupia nepalí	NPR	524
ISLAS COOK (LAS)	Dólar de la Islas Cook	NZD	554
NUEVA ZELANDA	Dólar neozelandés	NZD	554
NIUE	Dólar neozelandés	NZD	554
PITCAIRN	Dólar neozelandés	NZD	554
TOKELAU	Dólar neozelandés	NZD	554
OMÁN	Rial omaní	OMR	512
PANAMÁ	Balboa	PAB	590
PERU	Nuevo Sol	PEN	604
PAPÚA NUEVA GUINEA	Kina	PGK	598
FILIPINAS	Peso filipino	PHP	608
PAKISTÁN	Rupia pakistaní	PKR	586
POLONIA	Zloty	PLN	985
PARAGUAY	Guaraní	PYG	600
QATAR	Riyal catarí	QAR	634
RUMANIA	Leu rumano	RON	946
SERBIA	Dinar serbio	RSD	941
RUSIA	Rublo ruso	RUB	643
RUANDA	Franco ruandés	RWF	646
ARABIA SAUDITA	Riyal saudí	SAR	682
ISLAS SALOMÓN	Dólar de Islas Salomón	SBD	090
SEYCHELLES	Rupia de Seychelles	SCR	690
SUDÁN	Libra sudanesa	SDG	938
SUECIA	Corona sueca	SEK	752
SINGAPUR	Dólar de Singapur	SGD	702
SANTA HELENA ASCENCIÓN Y TRISTÁN DE ACUÑA	Libra de Santa Helena	SHP	654
SIERRA LEONA	Leone	SLL	694
SOMALIA	Chelín somalí	SOS	706
SURINAM	Dólar de Surinam	SRD	968
SUDÁN DEL SUR	Libra sursudanesa	SSP	728
SAN TOMÉ Y PRÍNCIPE	Dobra	STD	678
EL SALVADOR	Colón	SVC	222
REPÚBLICA ÁRABE SIRIA	Libra siria	SYP	760
SUAZILANDIA	Lilangeni	SZL	748
TAILANDIA	Baht	THB	764
TAJIKISTÁN	Somoni	TJS	972
TURMENISTÁN	Manat turcomano	TMT	934
TÚNEZ	Dinar tunecino	TND	788
TONGA	Pa’anga	TOP	776
TURQUÍA	Lira turca	TRY	949
TRINIDAD Y TOBAGO	Dólar de Trinidad y Tobago	TTD	780
TAIWÁN (PROVINCIA DE CHINA)	Nuevo dólar de Taiwán	TWD	901
REPÚBLICA UNIDA DE TANZANIA	Chelín tanzano	TZS	834
UKRANIA	Grivnia	UAH	980
UGANDA	Chelín ugandés	UGX	800
SAMOA AMERICANA	Dólar estadounidense	USD	840
BONAIRE, SAN EUSTAQUIO Y SABA	Dólar estadounidense	USD	840
TERRITORIO BRITÁNICO DEL OCÉANO ÍNDICO	Dólar estadounidense	USD	840
ECUADOR	Dólar estadounidense	USD	840
EL SALVADOR	Dólar estadounidense	USD	840
GUAM	Dólar estadounidense	USD	840
HAITÍ	Dólar estadounidense	USD	840
ISLAS MARSHALL	Dólar estadounidense	USD	840
MICRONESIA	Dólar estadounidense	USD	840
ISLAS MARIANS DEL NORTE	Dólar estadounidense	USD	840
PALAU	Dólar estadounidense	USD	840
PANAMÁ	Dólar estadounidense	USD	840
PUERTO RICO	Dólar estadounidense	USD	840
TIMOR ORIENTAL	Dólar estadounidense	USD	840
ISLAS TURCOS Y CAICOS	Dólar estadounidense	USD	840
ISLAS ULTRAMARINAS MENORES DE EE. UU.	Dólar estadounidense	USD	840
ESTADOS UNIDOS DE AMÉRICA	Dólar estadounidense	USD	840
ISLAS VÍRGENES BRITÁNICAS	Dólar estadounidense	USD	840
ISLAS VÍRGENES (EEUU)	Dólar estadounidense	USD	840
ESTADOS UNIDOS DE AMÉRICA	Dólar estadounidense (Next day)	USN	997
URUGUAY	Peso uruguayo en unidades indexadas (URUIURUI)	UYI	940
URUGUAY	Peso uruguayo	UYU	858
UZBEKISTÁN	Som uzbeko	UZS	860
REPÚBLICA BOLIVARIANA DE VENEZUELA	Bolívar	VEF	937
VIETNAM	Dong	VND	704
VANUATU	Vatu	VUV	548
SAMOA	Tala	WST	882
CAMERÚN	Franco CFA de África Central	XAF	950
REPÚBLICA CENTROAFRICANA (LA)	Franco CFA de África Central	XAF	950
CHAD	Franco CFA de África Central	XAF	950
CONGO (EL)	Franco CFA de África Central	XAF	950
GUINEA ECUATORIAL	Franco CFA de África Central	XAF	950
GABÓN	Franco CFA de África Central	XAF	950
ANGUILLA	Dólar del Caribe Oriental	XCD	951
ANTIGUA Y BARBUDA	Dólar del Caribe Oriental	XCD	951
DOMINICA	Dólar del Caribe Oriental	XCD	951
GRANADA	Dólar del Caribe Oriental	XCD	951
MONTSERRAT	Dólar del Caribe oriental	XCD	951
SAN CRISTÓBAL Y NIEVES	Dólar del Caribe oriental	XCD	951
SANTA LUCÍA	Dólar del Caribe oriental	XCD	951
SAN VICENTE Y LAS GRANADINAS	Dólar del Caribe oriental	XCD	951
FONDO MONETARIO INTERNACIONAL	SDR (Derecho Especial de Retiro)	XDR	960
BENÍN	Franco CFA de África Occidental	XOF	952
BURKINA FASO	Franco CFA de África Occidental	XOF	952
COSTA DE MARFIL	Franco CFA de África Occidental	XOF	952
GUINEA-BISSAU	Franco CFA de África Occidental	XOF	952
MALÍ	Franco CFA de África Occidental	XOF	952
NIGERIA	Franco CFA de África Occidental	XOF	952
SENEGAL	Franco CFA de África Occidental	XOF	952
TOGO	Franco CFA de África Occidental	XOF	952
POLINESIA FRANCESA	Franco CFP	XPF	953
NUEVA CALEDONIA	Franco CFP	XPF	953
WALLIS Y FUTUNA	Franco CFP	XPF	953
SISTEMA UNITARIO DE COMPENSACION REGIONAL DE PAGOS "SUCRE"	Sucre	XSU	994
PAISES MIEMBROS DEL BANCO AFRICANO DE DESARROLLO	BAD UNIDAD DE CUENTAS	XUA	965
YEMEN	Rial yemení	YER	886
LESOTO	Rand	ZAR	710
NAMIBIA	Rand	ZAR	710
SUDÁFRICA	Rand	ZAR	710
ZAMBIA	Kwacha zambiano	ZMW	967
ZIMBABUE	Dólar zimbabuense	ZWL	932
'''
comp = (
 "USD", 
 "AED", 
 "AFN", 
 "ALL", 
 "AMD", 
 "ANG", 
 "AOA", 
 "ARS", 
 "AUD", 
 "AWG", 
 "AZN", 
 "BAM", 
 "BBD", 
 "BDT", 
 "BGN", 
 "BHD", 
 "BIF", 
 "BMD", 
 "BND", 
 "BOB", 
 "BRL", 
 "BSD", 
 "BTN", 
 "BWP", 
 "BYN", 
 "BZD", 
 "CAD", 
 "CDF", 
 "CHF", 
 "CLP", 
 "CNY", 
 "COP", 
 "CRC", 
 "CUP", 
 "CVE", 
 "CZK", 
 "DJF", 
 "DKK", 
 "DOP", 
 "DZD", 
 "EGP", 
 "ERN", 
 "ETB", 
 "EUR", 
 "FJD", 
 "FKP", 
 "FOK", 
 "GBP", 
 "GEL", 
 "GGP", 
 "GHS", 
 "GIP", 
 "GMD", 
 "GNF", 
 "GTQ", 
 "GYD", 
 "HKD", 
 "HNL", 
 "HRK", 
 "HTG", 
 "HUF", 
 "IDR", 
 "ILS", 
 "IMP", 
 "INR", 
 "IQD", 
 "IRR", 
 "ISK", 
 "JEP", 
 "JMD", 
 "JOD", 
 "JPY", 
 "KES", 
 "KGS", 
 "KHR", 
 "KID", 
 "KMF", 
 "KRW", 
 "KWD", 
 "KYD", 
 "KZT", 
 "LAK", 
 "LBP", 
 "LKR", 
 "LRD", 
 "LSL", 
 "LYD", 
 "MAD", 
 "MDL", 
 "MGA", 
 "MKD", 
 "MMK", 
 "MNT", 
 "MOP", 
 "MRU", 
 "MUR", 
 "MVR", 
 "MWK", 
 "MXN", 
 "MYR", 
 "MZN", 
 "NAD", 
 "NGN", 
 "NIO", 
 "NOK", 
 "NPR", 
 "NZD", 
 "OMR", 
 "PAB", 
 "PEN", 
 "PGK", 
 "PHP", 
 "PKR", 
 "PLN", 
 "PYG", 
 "QAR", 
 "RON", 
 "RSD", 
 "RUB", 
 "RWF", 
 "SAR", 
 "SBD", 
 "SCR", 
 "SDG", 
 "SEK", 
 "SGD", 
 "SHP", 
 "SLL", 
 "SOS", 
 "SRD", 
 "SSP", 
 "STN", 
 "SYP", 
 "SZL", 
 "THB", 
 "TJS", 
 "TMT", 
 "TND", 
 "TOP", 
 "TRY", 
 "TTD", 
 "TVD", 
 "TWD", 
 "TZS", 
 "UAH", 
 "UGX", 
 "UYU", 
 "UZS", 
 "VES", 
 "VND", 
 "VUV", 
 "WST", 
 "XAF", 
 "XCD", 
 "XDR", 
 "XOF", 
 "XPF", 
 "YER", 
 "ZAR", 
 "ZMW", 
 "ZWL"
)
a = re.findall(r'\s*(\D+)\s([A-Z]{3})\s\d+', text, flags= re.MULTILINE)
dicc = {coin: mean.split('\t')[1] if coin in comp else None for mean, coin in a }
dele = []
for key, mean in dicc.items():
    if mean == None:
       dele.append(key)
for x in dele:
    del dicc[x]
[print(str(x.strip())+':',str(y.strip())) for x,y in dicc.items()]
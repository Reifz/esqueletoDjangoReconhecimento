DESCRIBE usuario;



id_usuario	int(15)	NO	PRI	NULL	auto_increment	
nome	varchar(155)	NO		NULL		
email	varchar(155)	NO		NULL		
cracha	varchar(100)	YES		NULL		
foto	text	YES		NULL		
nivel_acesso	int(3)	YES		NULL		



DESCRIBE logacesso;

id_log	int(25)	NO	PRI	NULL	auto_increment	
id_usuario	int(15)	YES		NULL		
resultado	text	YES		NULL		
data_hora	datetime	YES		current_timestamp()		

# RDMBS ...
OD_table _odt

# java
calc_cost
calc_path

# java
request_shortest_path(name)
	connect_str = 'connect.id=$$$, pwd=$$$';
	con = odbc.open(connect_str);

	records = con.query('select * from od_links where ...')
 	
 	...

 	calc_cost
 	calc_path



#!/usr/bin/perl
use XBase; # модуль работы с БД в формате DBF
use Encode;
use lib './lib';
use freshdb;
use Data::Dumper;
my $filedir='../files/dbf_daemon';
my $db=freshdb->new(host=>'localhost',db_name=>'crm',user=>'crm',password=>'');
$db->{connect}->do("set names utf8");
while(1){
    my $rec=$db->query(query=>'select * from dbf_daemon where ready=1 order by id limit 1',onerow=>1);
    if($rec){
        file_create($rec);
        #exit;
    }
    else{
        sleep 2;
    }
    #pre(); 
    #exit;
}

sub file_create{
    my $rec=shift;
    my $data=$db->query(
        query=>q{
            SELECT
                ap.header plan_name, g.header, g.code
            FROM
                action_plan ap
                join action_plan_good apg ON apg.action_plan_id=ap.id
                join good g ON g.id=apg.good_id
            WHERE ap.id=? order by g.header
        },
        values=>[$rec->{action_plan_id}]
    );
    unlink("$filedir/$rec->{id}.dbf");
    my $table = XBase->create(
        name=>"$filedir/$rec->{id}.dbf",
        field_names =>    [ "plan_name", "header", "code"],
        field_types =>    [    "C",     "C",    "C"],
        field_decimals => [  undef,   undef,  undef],
        field_lengths =>  [   255,      255,     30],

    )  or die XBase->errstr; # обработка ошибок
    my $recno = 0; # добавляемые записи нумеруются с нуля

    my $number=1;
    foreach my $d (@{$data}){
        #pre($d);
        #foreach ( keys(%{$d})) {
            Encode::from_to($d->{plan_name},'utf8','cp866');
            Encode::from_to($d->{header},'utf8','cp866');
            Encode::from_to($d->{code},'utf8','cp866');
        #}
        #pre(["$number", $d->{plan_name}, $d->{header}, $d->{code}]);
        $table->set_record($number, $d->{plan_name}, $d->{header}, "$d->{code}"); 
        # $table->set_record_hash(
        #         "plan_name" => $d=>{plan_name},
        #         "header"=>$d->{header},
        #         "code"=>$d->{code}
        # );
        $number++;
        
    }

    $table->close();
    $db->query(
        query=>"UPDATE dbf_daemon set ready=1 where id=$rec->{id}"
    );
}
sub pre{
    print Dumper($_[0])
}
#my ($id, $name, $latin, $area) = split(';', $data);

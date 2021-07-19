package freshdb;
#use Scalar::Util qw/refaddr/;
use Data::Dumper;
use DBI;
use Encode;

use lib '/var/www/lib';


my %items;
sub new {
  my($class,%args) = @_;
  my $self = bless {}, $class;
  if($args{host}){
    $self->{connect}=cdb2(%args);
  }
  elsif($args{connect_name}){
    $self->{connect}=cdb($args{connect_name});
  }
  else{
    die('not set connect_name')
  }
  
  $self->{model_method}=$args{model_method};
  $self->{confdir}=$args{confdir};
    return $self;
}

sub get_form_from_conf{
    my $file=shift;
    open F, $file;
    my $conf='';
    while(<F>){
        $conf.=$_;
    }
    close F;
    my %form;
    $conf=~s/^.*(^|\n)\s*our\s*\%form/\%form/gs;
    $conf=~s!(\n|^|\s)(use|requere)\s*.+?;!!gs;

    eval($conf);
    die $@ if($@);

    return \%form;
};

sub get{
    my ($self,%args)=@_;
    my $opt=\%args;
    
    $opt->{connect}=$self->{connect};
    if($self->{model_method} eq 'conf' && $self->{confdir} && $opt->{struct} && !$opt->{table_id}){
        #print "111\n";
        unless(-e qq{$self->{confdir}/$opt->{struct}}){
            die "file '$self->{confdir}/$opt->{struct}' not found\n";            
        }
        $self->{form}=&get_form_from_conf(qq{$self->{confdir}/$opt->{struct}});
        $opt->{table_id} = $self->{form}->{work_table_id};
        $opt->{table} = $self->{form}->{work_table};
        if($opt->{use_model} && !$opt->{select_fields}){
            $opt->{table}.=' wt';
            my @sf=("wt.$opt->{table_id} id"); # select_fields massive
            my $tnumber=1;
            
            foreach my $field (@{$self->{form}->{fields}}){
                    if($field->{type} eq 'file'){
                        my $fd=$field->{filedir};
                        $fd=~s/^\.\.\//\//;
                        push @sf, qq{concat('$fd/',wt.$field->{name}) as $field->{name}_and_path};
                        my $i=1;
                        while($field->{converter}=~m/output_file=['"](.+?)['"]/gs){
                            my $out=$1;
                            next if ($out eq '[%input%].[%input_ext%]');
                            $out=~s/\.\[%input_ext%\]/\[%input_ext%\]/;
                            $out=~s/(\]|^)([^\[]+)\[/$1,'$2',\[/;

                            $out=~s/\[%input%\]/substring_index(wt.$field->{name},'.',1)/;
                            $out=~s/\[%input_ext%\]/'\.',substring_index(wt.$field->{name},'.',-1)/;
                            push @sf, qq{concat('$fd/',$out) as $field->{name}_and_path_mini$i};
                            $i++;
                        }
                    }
                    elsif($field->{type} eq 'select_values'){
                            my $case='';
                            $case.=qq{, CASE $field->{name} };
                            while($field->{values}=~m/([^;]+?)=>([^;]+)/gs){
                                $case.=qq{WHEN '$1' then '$2' }
                            }
                            $case.=qq{ END as `$field->{name}`};
                            push @sf, $case;
                    }
                    elsif($field->{type} eq 'select_from_table'){
                        my $alias=qq{t$tnumber};
                        
                        $opt->{table}.=qq{ LEFT JOIN $field->{table} $alias ON (wt.$field->{name} = $alias.$field->{value_field})};
                        push @sf, qq{$alias.$field->{header_field} $field->{name},  $alias.$field->{value_field} $field->{name}_value};
                        $tnumber++;
                    }
                    elsif($field->{type} eq 'text' || $field->{type} eq 'textarea' || $field->{type} eq 'checkbox'){
                        push @sf, qq{wt.$field->{name}};    
                    }
            }
            $opt->{select_fields} = join(', ',@sf);
            #print "sf: $opt->{select_fields}";
                
        }
        
        #print Dumper($self->{form});
        #exit;
                
    }
    else{
        
        $opt->{table_id} = 'id' if(!$opt->{table_id});
    }
    $opt->{select_fields}='*' unless($opt->{select_fields});
    $table=$opt->{table} if($opt->{table});
    if($opt->{id}=~m/^\d+$/){
        $table=$opt->{where}='id = '.$opt->{id};
        $opt->{onerow}=1 unless($opt->{onevalue})
    }
    
    my $query="SELECT $opt->{select_fields} FROM $opt->{table} ";
    $query.=qq{ WHERE $opt->{where}} if($opt->{where});
    $query.=qq{ GROUP BY $opt->{group}} if($opt->{group});
    $query.=qq{ ORDER BY $opt->{order}} if($opt->{order});
    $query.=qq{ LIMIT $opt->{limit}} if($opt->{limit}=~m/^\d+(,\d+)?$/);
    
    if($opt->{debug}){
        print "QUERY:\n$query\n".Dumper($opt->{values});
    }
    my $result;
    my $sth;
    eval(q{
        $sth=$opt->{connect}->prepare($query);
        $sth->execute(@{$opt->{values}}) || die($dbh->{error_str});
    });
    if($@){
        print "Error_query:\n$query\n";
        print Dumper($opt->{values});
        exit;
  }
  if($opt->{onevalue}){
    $result=$sth->fetchrow();
  }
  elsif($opt->{get_hash}){
    $result=$sth->fetchall_hashref($opt->{get_hash})
  }
    elsif($opt->{massive}){
        my $mas=[];
        my $cnt_rows=$sth->rows();
        foreach (1..$cnt_rows){
            my $v=$sth->fetchrow();
            push @{$mas},$v;
        }
        return $mas;
    }
    elsif($opt->{onerow}){
        $result=$sth->fetchrow_hashref();
    }
    else{        
        $result=$sth->fetchall_arrayref({});
    }
    return $result;
}
sub cdb2{ # коненскт
  my %opt=@_;
  my $c=\%opt;
  $connect=DBI->connect("DBI:mysql:$c->{db_name}:$c->{host}",$c->{user},$c->{password}, , { mysql_auto_reconnect=>1, }) || die($c); # RaiseError => 1,
  #$connect->{'mysql_enable_utf8'} = 1;
  $connect->do("SET names $c->{CHARSET_DB}") if($c->{CHARSET_DB});
  return $connect;
}
sub cdb{ # свой CDB специально для трейда
  my $name=shift;
  my $code=q{our $}.$name.";\n";
  our ($DBhost_auto_tenders,$SPH_TENDERS_MYSQL,$read_DB_protocols,$sph_RT,$DBhost_semc);
  
  open F, '/www/connectDB.conf';
    while(<F>){$code.=$_}
    close F;
    eval($code);
  #my $host=$$name;
  if($name eq 'DBhost_semc'){
    $c={
      CHARSET_DB=>'utf8',
      DBuser=>'rosexport',
      DBpassword=>'',
      DBname=>'semc_kru_new',
      DBhost=>$$name
    };
  }
  elsif($name=~m/^(read_DBhost|DBhost|read_DB_protocols)$/){
    
    $c={
      CHARSET_DB=>'utf8',
      DBuser=>'rosexport',
      DBpassword=>'',
      DBname=>($name=~m/protocols/)?'protocols':'rosexport',
      DBhost=>$$name
    };
    
  }
  elsif($name eq 'rosexport_katalog_archive'){
    $c={
      CHARSET_DB=>'utf8',
      DBuser=>'rosexport',
      DBpassword=>'',
      DBname=>'rosexport_katalog_archive',
      DBhost=>$$name
    };
  }
  elsif($name eq 'protocols_write'){
    $c={
      CHARSET_DB=>'utf8',
      DBuser=>'rosexport',
      DBpassword=>'',
      DBname=>'protocols',
      DBhost=>$DB_protocols
    };
  }
  elsif($name eq 'protocols_records'){
    $c={
      CHARSET_DB=>'utf8',
      DBuser=>'rosexport',
      DBpassword=>'',
      DBname=>'protocols_records',
      DBhost=>'192.168.0.121'
    };
  }
  elsif($name eq 'DBhost_subscribe'){
    $c={
      CHARSET_DB=>'utf8',
      DBuser=>'rosexport',
      DBpassword=>'',
      DBname=>'subscribe',
      DBhost=>$$name
    };
  }
  elsif($name eq 'mail_DBhost'){
    $c={
      CHARSET_DB=>'utf8',
      DBuser=>'rosexport',
      DBpassword=>'',
      DBname=>'mail',
      DBhost=>$$name
    };
  }
  elsif($name eq 'supplier'){
    $c={
          CHARSET_DB=>'utf8',
          DBuser=>'supplier',
          DBpassword=>'',
          DBname=>'supplier',
          DBhost=>'192.168.0.101'
    }
  }
  elsif($name eq 'backup'){
    $c={
          CHARSET_DB=>'utf8',
          DBuser=>'rosexport',
          DBpassword=>'',
          DBname=>'temp',
          DBhost=>'192.168.0.71'
    }
  }
  elsif($name eq 'DBhost_auto_tenders_read'){
    
    $c={
      CHARSET_DB=>'utf8',
      DBuser=>'rosexport',
      DBpassword=>'',
      DBname=>'auto_tenders',
      DBhost=>$DBhost_auto_tenders
    }
  }
  elsif($name eq 'spam'){
    $c={
      CHARSET_DB=>'utf8',
      DBuser=>'auz',
      DBpassword=>'',
      DBname=>'spam',
      DBhost=>'185.76.253.230'
    }
  }
  elsif($name eq 'rosexport_pattern'){
    $c={
      CHARSET_DB=>'utf8',
      DBuser=>'rosexport',
      DBpassword=>'',
      DBname=>'rosexport_pattern',
      DBhost=>'192.168.0.117'
    }
  }
  elsif($name=~m{^(SPH_TENDERS_MYSQL|SPH_RT)$}){
    $c={
      CHARSET_DB=>'utf8',
      DBuser=>'sphinx',
      DBpassword=>'',
      DBname=>'sphinx',
      DBhost=>$$name
    };
  }
  elsif($name eq 'svcms'){
    $c={
      CHARSET_DB=>'utf8',
      DBuser=>'svcms',
      DBpassword=>'',
      DBname=>'svcms',
      DBhost=>'192.168.0.41'
    };
  }
  $connect=DBI->connect("DBI:mysql:$c->{DBname}:$c->{DBhost}",$c->{DBuser},$c->{DBpassword}, , { mysql_auto_reconnect=>1, }) || die($c); # RaiseError => 1,
  #$connect->{'mysql_enable_utf8'} = 1;
  $connect->do("SET names $c->{CHARSET_DB}") if($c->{CHARSET_DB});
  return $connect;
}


sub save{
    my ($self,%args)=@_;
    my $opt=\%args;
    $opt->{connect}=$self->{connect};
    $opt->{table} if($opt->{table});
    my $dumpdata=undef;
  #print "desc $opt->{table}\n";
    my $sth=$self->{connect}->prepare("desc $opt->{table}");
    $sth->execute();
    my @fields=(); my @values_fn=(); my @values_exec=();
    #print Dumper($opt->{data});
    foreach my $desc (@{$sth->fetchall_arrayref({})}){
        next if($desc->{Key} eq 'auto_increment');
        my $field=lc($desc->{Field});
        
        foreach my $field_data (keys(%{$opt->{data}})){    
            if($field eq lc($field_data)){
                #print "$field / $opt->{data}->{$field_data}\n";
                my $value=$opt->{data}->{$field_data};
                next unless(defined($value));
                Encode::_utf8_off($value) unless($opt->{not_encode});
                #print "$desc->{Field} /  $value\n";            
                if($opt->{update}){
                    if($value=~m/^func::(.+)/){
                        push @fields,qq{$desc->{Field}=$1};
                        push @{$dumpdata},{$desc->{Field}=>$1};
                    }
                    else{
                        push @fields,qq{$desc->{Field}=?};
                        push @values_exec,$value;
                        push @{$dumpdata},{$desc->{Field}=>$value};
                    }
                }
                else{
                
                    push @fields,$desc->{Field};
                    if($value=~m/^func::(.+)/){
                        push @values_fn,$1;
                        push @{$dumpdata},{$desc->{Field}=>$1};
                    }
                    else{
                        push @values_fn,'?';
                        push @values_exec,$value;
                        push @{$dumpdata},{$desc->{Field}=>$value};
                    }
                }
            }
        }        
    }
    
    my $command; my $query;
    if($opt->{update} && $opt->{where}){
        $query="UPDATE $opt->{table} SET ".join(', ',@fields)." WHERE $opt->{where}";
    }
    else
    {
        if($opt->{on_replace} || $opt->{replace}){
            $command='REPLACE';
        }
        elsif($opt->{insert_ignore}){
            $command='INSERT IGNORE';
        }
        else{
            $command='INSERT';
        }
        $query="$command INTO $opt->{table}(".join(',',@fields).") VALUES(".join(',',@values_fn).")";
    }
    
    
    @values_exec=(@values_exec,@{$opt->{values}});
    if($opt->{debug}){
        print "QUERY:\n$query\n".Dumper($dumpdata)."\n";
    }
    eval q{
        $sth=$self->{connect}->prepare($query);
        $sth->execute(@values_exec);
    };
    
    if($@){
        print "Error_query:\n$query\n";
        #print Dumper(@values_exec);
        print "<br>$@";
        die($@); # !!!!! fdds: переписал вместо exit !!!!!
    }
    $sth->{mysql_insertid}
}
sub query{
    my ($self,%args)=@_;
    my $opt=\%args;
  return if($opt->{sublevel}>10);
  
    if($opt->{tree_use}){
      unless($opt->{query}=~m/parent_id\s*(=|is)/){ # Если parent_id не указан -- прифигачиваем фиктивный parent_id
          if($opt->{query}=~/(\s+where\s+)/i){
            $opt->{query}=~s/(\s+where\s+)/ WHERE (parent_id IS null) AND /i;
          }
          elsif($opt->{query}=~/\s+order\s+by/i){
            $opt->{query}=~s/(\s+order\s+by\s+)/ WHERE parent_id is null $1/i;
          }
          else{
            $opt->{query}.=qq{ WHERE (parent_id is null)}
          }
      }
  }
  
    if($opt->{debug}){
    print "$opt->{query}<br>\n";
    print Dumper($opt->{values});
  }
    my $res;

  my $sth=$self->{connect}->prepare($opt->{query});
    $sth->execute(@{$opt->{values}});
    if($opt->{query}=~m/^\s*select/is){
    if($opt->{onerow}){
      $res=$sth->fetchrow_hashref;
    }
    elsif($opt->{onevalue}){
      $res=$sth->fetchrow;
    }
        elsif($opt->{massive}){
            
            my @a=();
            while(my $item=$sth->fetchrow_hashref()){            
                    my $k=(keys(%{$item}))[0]; push @a,$item->{$k};
            }
            $res=\@a;
            
        }
    elsif($opt->{get_hash}){
      $res=$sth->fetchall_hashref($opt->{get_hash})
    }
        elsif($opt->{hash}){
            my %h=();
            while(my $item=$sth->fetchrow_hashref()){            
                    my $k=(keys(%{$item}))[0]; $h{$item->{$k}}=1;
            }
            $res=\%h;
        }
    else{
      $res=$sth->fetchall_arrayref({});
    }
    $sth->finish();
    
    #print "x: ".(($opt->{tree_use} && ($opt->{depth}<$opt->{max_depth} || !defined $opt->{max_depth})));
    # TREE USE
        if($opt->{tree_use} && ($opt->{depth}<$opt->{max_depth} || !defined $opt->{max_depth})){

      if(defined $opt->{depth}){
                $opt->{depth}++;
            }
            else{
                $opt->{depth}=1 unless defined($opt->{depth});
            }
            if($opt->{massive}){
                my @new_res=();
                foreach my $id (@{$res}){
                    $opt->{query}=~s/(parent_id\s*=\s*|parent_id\s+is\s+)[^\s]+/$1$id/is;
                    my %optx=%{$opt};
                    @new_res=(@new_res,$self->run_query(%optx));
                }
                @{$res}=($res,@new_res);
            }
            else{
                if($opt->{tree_to_massive}){
                    my @new_res=();
                    foreach my $r (@{$res}){
                        $opt->{query}=~s/where.+?(parent_id\s*=\s*)[^\s]+/where $1$r->{id}/is;
            $opt->{values}=[];
                        my $nr = $self->run_query(%{$opt});
                        @new_res=(@new_res,@{$self->run_query(%{$opt})});
                    }
                    #print Dumper(@new_res);
                    @{$res}=(@{$res},@new_res);
                }
                else{
          #print Dumper($res);
          #exit;
                    foreach my $r (@{$res}){
            $opt->{sublevel}++;

            $opt->{values}=[];
                        $opt->{query}=~s/where.+?(parent_id\s*(=|is)\s*)[^\s]+/where parent_id = $r->{id}/is;                    
            #print "run_query: ".print Dumper($opt); exit;
                        $r->{child}=$self->run_query(%{$opt});
                    }
                }
            }        
        }
    return $res;
  }
}
return 1;
END { }

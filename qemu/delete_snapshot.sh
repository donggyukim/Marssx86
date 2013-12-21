for i in {1..50} ; do 
	./qemu-img snapshot -d $i ~/disk/spec2006.qcow2
done

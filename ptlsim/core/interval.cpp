#include <interval.h>

extern ofstream interval_file;

void FMTEntry::reset() {
	robid = -1;
	mispredict = false;
	local_branch = 0;
	local_icache_hit = 0;
	local_l1_icache = 0;
	local_l2_icache = 0;
	local_itlb = 0;
	local_frontend = 0;
}

ostream& FMTEntry::print(ostream& os) const{
	os << "index: " << index() << ", robid: " << robid;
	return os;
}

FMTEntry& FMTEntry::operator =(FMTEntry &fmt){
	robid = fmt.robid;
	mispredict = fmt.mispredict;
	local_branch = fmt.local_branch;
	local_icache_hit = fmt.local_icache_hit;
	local_l1_icache = fmt.local_l1_icache;
	local_l2_icache = fmt.local_l2_icache;
	return *this;
}

// Interval constructor
Interval::Interval() {
	// global counter initialization
	global_branch = 0;
	global_icache_hit = 0;
	global_l1_icache = 0;
	global_l2_icache = 0;
	global_dcache_hit = 0;
	global_l1_dcache = 0;
	global_l2_dcache = 0;
	global_itlb = 0;
	global_dtlb = 0;
	global_long_lat = 0;
	global_frontend = 0;
	global_backend = 0;

	reset();
}

// reset FMT
void Interval::reset() {
	FMT.reset();
	dispatch_tail = FMT.head;

	// for debug
	//ptl_logfile << "reset!!!!!!!"<<endl;
}

// FMT entry allocation
void Interval::fmt_entry_alloc(){
	FMT.alloc();

	//for debug
	//ptl_logfile << "after fetch : dispatch tail : " << dispatch_tail << " " << FMT;
}

// dispatch tail pointer advance
void Interval::branch_dispatch(W16s robid){
	FMT[dispatch_tail].set_robid(robid);
	dispatch_tail = add_index_modulo(dispatch_tail, +1, FMT_SIZE);

	//for debug
	//ptl_logfile << "after dispatch : dispatch tail : " << dispatch_tail << " " << FMT;
}

//I$ hit count
void Interval::icache_hit(){
	FMTEntry* fmt = FMT.peek();

	if unlikely (fmt == NULL)
		global_icache_hit++;
	else
		fmt->local_icache_hit++;
}

//L1 I$ miss count
void Interval::l1_icache_miss(){
	FMTEntry* fmt = FMT.peek();

	if unlikely (fmt == NULL)
		global_l1_icache++;
	else
		fmt->local_l1_icache++;
}

//L2 I$ miss count
void Interval::l2_icache_miss(){
	FMTEntry* fmt = FMT.peek();

	if unlikely (fmt == NULL)
		global_l2_icache++;
	else
		fmt->local_l2_icache++;
}

//ITLB miss count
void Interval::itlb_miss(){
	FMTEntry* fmt = FMT.peek();

	if unlikely (fmt == NULL)
		global_itlb++;
	else
		fmt->local_itlb++;
}

//frontend miss count
void Interval::frontend_miss(){
	FMTEntry* fmt = FMT.peek();

	if unlikely (fmt == NULL)
		global_frontend++;
	else
		fmt->local_frontend++;
}

// when branch misprediction resolves
void Interval::branch_mispred(W16s robid){

	// for debug
	if unlikely (FMT.empty() || FMT.head == dispatch_tail){
		ptl_logfile << "Interval: branch mispredicton error!" << endl;
		ptl_logfile << "Precondition false!" << endl;
		return;
	}

	// for debug
	//ptl_logfile << "Interval: misprediction of " << robid << endl;

	int idx = add_index_modulo(dispatch_tail, -1, FMT_SIZE);
	FMTEntry* start_fmt = &FMT[idx];
	
	foreach_backward_from(FMT, start_fmt, i){
		FMTEntry& fmt = FMT[i];

		if unlikely (fmt.match(robid)){
			if likely (!fmt.mispredict){
				// branch misprediction 
				// --> FMT entry's misprediction bit set
				fmt.mispredict = true;
				// add local branch miss cycles to the global branch counter
				global_branch += fmt.local_branch;
				annul(robid);
			}
			return;
		}
	}
	
	// for debug
	ptl_logfile << "Interval: branch_mispred error!" << endl;
	ptl_logfile << "Postcondition false!" << endl;
}

// when branch is redispatched
void Interval::branch_redispatch(W16s robid){
	// for debug
	//ptl_logfile << "Interval : redispatch " << robid << endl;
	//ptl_logfile << "before redispatch : " << FMT;

	if (FMT.empty() || FMT.head == dispatch_tail){
		//ptl_logfile << "Interval : redispatch error!" << endl;
		//ptl_logfile << "Precondition false!" << endl;
		return;
	}

	int idx = add_index_modulo(dispatch_tail, -1, FMT_SIZE);
	FMTEntry* start_fmt = &FMT[idx];

	foreach_backward_from(FMT, start_fmt, i){
		FMTEntry& fmt = FMT[i];

		if unlikely (fmt.match(robid)){
			fmt_entry_remove(&fmt);
			dispatch_tail = add_index_modulo(dispatch_tail, -1, FMT_SIZE);
			fmt_entry_alloc();

			// for debug
			//ptl_logfile << "after redispatch : " << FMT;
			return;
		}
	}

	// for debug	
	//ptl_logfile << "Interval: redispatch error!" << endl;
	//ptl_logfile << "Postcondition false!" << endl;
}

//called by redispatch
void Interval::fmt_entry_remove(FMTEntry* target_fmt){
	int next_idx;

	// move entries by 1
	foreach_forward_from(FMT, target_fmt, idx){
		if(idx == FMT.tail) break;

		next_idx = add_index_modulo(idx, +1, FMT_SIZE);
		FMTEntry& fmt = FMT[idx];
		FMTEntry& fmt_next = FMT[next_idx];
		fmt = fmt_next;
	}

	// remove tail
	FMTEntry* fmt = FMT.peektail();
	fmt->reset();
	FMT.annul(fmt);
}

// annul FMT
void Interval::annul(W16s robid){
	
	if (FMT.empty()){
		ptl_logfile << "Interval: annul error!" << endl;
		ptl_logfile << "Precondition false!" << endl;
		return;
		assert(false);
	}

	//for debug
	//ptl_logfile << "before annul : dispatch tail : " << dispatch_tail << " " << FMT;

	// annul entries btwn fetch & dispatch tail pointers
	int idx = add_index_modulo(FMT.tail, -1, FMT_SIZE);
	int end_idx = add_index_modulo(dispatch_tail, -1, FMT_SIZE);;

	while (idx != end_idx) {
		FMTEntry& annulfmt = FMT[idx];
		annulfmt.reset();
		FMT.annul(annulfmt);
		idx = add_index_modulo(idx, -1, FMT_SIZE);
	}
	
	// annul entries btwn the entry pointed by dispatch tail
	// and the entry having 'robid'
	idx = add_index_modulo(dispatch_tail, -1, FMT_SIZE);
	end_idx = add_index_modulo(FMT.head, -1, FMT_SIZE);
	
	while (idx != end_idx) {
		FMTEntry& annulfmt = FMT[idx];

		if unlikely (annulfmt.match(robid)){
			//for debug
			//ptl_logfile << "after annul : dispatch tail : " << dispatch_tail << " " << FMT;
			return;
		}
		
		annulfmt.reset();
		FMT.annul(annulfmt);
		idx = add_index_modulo(idx, -1, FMT_SIZE);
		dispatch_tail = add_index_modulo(dispatch_tail, -1, FMT_SIZE);
	}
	
	ptl_logfile << "Interval: anull error! " << endl;
	ptl_logfile << "Postcondition false! " << endl;
}

// branch commit(or complete?)
// --> FMT entry deallocation
void Interval::fmt_entry_commit(W16s robid){
	
	FMTEntry* fmt = FMT.peek();

	if unlikely (fmt == NULL) {
		ptl_logfile << "Interval: FMT entry free error!" << endl;	
		ptl_logfile << "Precondition false!" << endl;	
		return;
	}

	while(fmt->robid != robid) {
		fmt->reset();
		FMT.pophead();
		fmt = FMT.peek();

		if unlikely (fmt == NULL) {
			ptl_logfile << "Interval: FMT entry free error!" << endl;	
			ptl_logfile << "Precondition false!" << endl;	
			return;	
		}
	}	
		
	// for debug	
	//ptl_logfile << "Interval: entry commit, from arg : " << robid << " from queue : " << fmt->robid << endl;

	if likely (!fmt->mispredict){
		global_icache_hit += fmt->local_icache_hit;
		global_l1_icache += fmt->local_l1_icache;
		global_l2_icache += fmt->local_l2_icache;
		global_itlb += fmt->local_itlb;
		global_frontend += fmt->local_frontend;	
	}
	
	fmt->reset();
	FMT.commit(fmt);
}

//count branch miss
void Interval::branch_miss()
{
	if (FMT.empty() || FMT.head == dispatch_tail)
		return;

	int idx = add_index_modulo(dispatch_tail, -1, FMT_SIZE);
	FMTEntry* start_fmt = &FMT[idx];

	foreach_backward_from(FMT, start_fmt, i){
		FMTEntry& fmt = FMT[i];
		
		if likely (!fmt.mispredict)
			fmt.local_branch++;
	}
}

void Interval::dump_interval(W16s core_id, W16s thread_id){
	W64 total_miss_cycle = global_icache_hit + global_dcache_hit
			+ global_l1_icache + global_l2_icache + global_itlb 
			+ global_l1_dcache + global_l2_dcache + global_dtlb 
			+ global_branch + global_frontend + global_backend;
	W64 base_cycle = sim_cycle - total_miss_cycle;

	interval_file << endl
		<< "Interval anlaysis (FMT) of core #" 
		<< core_id << " and thread #" << thread_id << endl
		<< "=======================" << endl
		<< "# of uOPs : \t" << total_uops_committed << endl
		<< "Base cycles : \t" << base_cycle << endl
		<< "I$ hit : \t" << global_icache_hit << endl
		<< "L1 I$ miss : \t" << global_l1_icache << endl
		<< "L2 I$ miss : \t" << global_l2_icache << endl
		<< "ITLB miss : \t" << global_itlb << endl
		<< "Frontend miss : \t" << global_frontend << endl
		<< "D$ hit : \t" << global_dcache_hit << endl
		<< "L1 D$ miss : \t" << global_l1_dcache << endl
		<< "L2 D$ miss : \t" << global_l2_dcache << endl
		<< "DTLB miss : \t" << global_dtlb << endl
		<< "Long lat miss : \t" << global_long_lat << endl
		<< "Backend miss : \t" << global_backend << endl
		<< "branch miss : \t" << global_branch << endl
		<< "Total miss cycles : \t" << total_miss_cycle << endl
		<< "Total cycles : \t" << sim_cycle << endl;
}

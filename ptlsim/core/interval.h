#ifndef _INTERVAL_H_
#define _INTERVAL_H_

#include <ptlsim.h>
#include <ooo-const.h>


struct FMTEntry
{
	int idx;
	bool entry_valid;

	W16s robid;
	bool mispredict;
	W64 local_branch;
	W64 local_icache_hit;
	W64 local_l1_icache;
	W64 local_l2_icache;
	W64 local_itlb;
	W64 local_frontend;

	void init(int idx_) { 
		idx = idx_; 
		reset(); 
	}
	void validate() { entry_valid = true; }
	int index() const { return idx; }

	void reset();
	void set_robid(W16s robid_) { robid = robid_; }
	bool match(W16s robid_) { return robid == robid_; }
	ostream& print(ostream& os) const; 
	FMTEntry& operator =(FMTEntry& fmt);
};

static inline ostream& operator <<(ostream& os, const FMTEntry& fmt){
	return fmt.print(os);
}

const int FMT_SIZE = OOO_ROB_SIZE + OOO_FETCH_Q_SIZE + 1;

struct Interval
{
	// Frontend Miss evnet Table
	Queue<FMTEntry, FMT_SIZE> FMT;

	// global counters
	W64 global_branch;
	W64 global_icache_hit;
	W64 global_l1_icache;
	W64 global_l2_icache;
	W64 global_itlb;
	W64 global_dcache_hit;
	W64 global_l1_dcache;
	W64 global_l2_dcache;
	W64 global_dtlb;
	W64 global_long_lat;
	W64 global_frontend;
	W64 global_backend;

	W64 prev_sim_cycle;

	int dispatch_tail;

	Interval();
	void reset();
	void fmt_entry_alloc();
	void fmt_entry_commit(W16s robid);
	void fmt_entry_remove(FMTEntry* target);
	void branch_dispatch(W16s robid);
	void branch_redispatch(W16s robid);
	void branch_miss();
	void branch_mispred(W16s robid);
	void annul(W16s robid);
	void after_flush() { global_branch++; };
	void icache_hit();
	void l1_icache_miss();
	void l2_icache_miss();
	void itlb_miss();
	void frontend_miss();
	void dcache_hit() { global_dcache_hit++; }
	void l1_dcache_miss() { global_l1_dcache++; }
	void l2_dcache_miss() { global_l2_dcache++; }
	void dtlb_miss() { global_dtlb++; }
	void backend_miss() { global_backend++; }
	void long_lat_miss() { global_long_lat++; }
	void dump_interval(W16s, W16s);
	void dump_periodic_interval(W16s, W16s);
};
#endif // _INTERVAL_H_

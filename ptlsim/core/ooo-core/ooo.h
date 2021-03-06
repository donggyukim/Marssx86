// -*- c++ -*-
//
// PTLsim: Cycle Accurate x86-64 Simulator
// Out-of-Order Core Simulator
//
// Copyright 2003-2008 Matt T. Yourst <yourst@yourst.com>
// Copyright 2006-2008 Hui Zeng <hzeng@cs.binghamton.edu>
// Copyright 2009-2010 Avadh Patel <apatel@cs.binghamton.edu>
//

#ifndef _OOOCORE_H_
#define _OOOCORE_H_

#include <ptlsim.h>
#include <basecore.h>
#include <branchpred.h>
#include <statelist.h>
#include <statsBuilder.h>
#include <decode.h>

#include <ooo-const.h>
#include <ooo-stats.h>

#include <interval.h> // by vteori

// With these disabled, simulation is faster
#define ENABLE_CHECKS
#define ENABLE_LOGGING
//#define ENABLE_CHECKS_IQ

// #define DISABLE_TLB

//
// Enable SMT operation:
//
// Note that this limits some configurations of resources and
// issue queues that would normally be possible in single
// threaded mode.
//

//#define ENABLE_SIM_TIMING
#ifdef ENABLE_SIM_TIMING
#define time_this_scope(ct) CycleTimerScope ctscope(ct)
#define start_timer(ct) ct.start()
#define stop_timer(ct) ct.stop()
#else
#define time_this_scope(ct) (0)
#define start_timer(ct) (0)
#define stop_timer(ct) (0)
#endif

#define CORE_STATS(var)							\
  getcore().core_stats.var(getthread().thread_stats.get_default_stats())

#define CORE_DEF_STATS(var)						\
  getcore().core_stats.var(getcore().getthread().thread_stats.get_default_stats())


namespace Memory{
  class MemoryHierarchy;
  class MemoryRequest;
}

namespace OOO_CORE_MODEL {

  using namespace Core;

  enum {
    FU_LDU0       = (1 << 0),
    FU_STU0       = (1 << 1),
    FU_LDU1       = (1 << 2),
    FU_STU1       = (1 << 3),
    FU_LDU2       = (1 << 4),
    FU_STU2       = (1 << 5),
    FU_LDU3       = (1 << 6),
    FU_STU3       = (1 << 7),
    FU_ALU0       = (1 << 8),
    FU_FPU0       = (1 << 9),
    FU_ALU1       = (1 << 10),
    FU_FPU1       = (1 << 11),
    FU_ALU2       = (1 << 12),
    FU_FPU2       = (1 << 13),
    FU_ALU3       = (1 << 14),
    FU_FPU3       = (1 << 15),
    FU_LDU4       = (1 << 16),
    FU_STU4       = (1 << 17),
    FU_LDU5       = (1 << 18),
    FU_STU5       = (1 << 19),
    FU_LDU6       = (1 << 20),
    FU_STU6       = (1 << 21),
    FU_LDU7       = (1 << 22),
    FU_STU7       = (1 << 23),
    FU_ALU4       = (1 << 24),
    FU_FPU4       = (1 << 25),
    FU_ALU5       = (1 << 26),
    FU_FPU5       = (1 << 27),
    FU_ALU6       = (1 << 28),
    FU_FPU6       = (1 << 29),
    FU_ALU7       = (1 << 30),
    FU_FPU7       = (1 << 31),
    FU_LDU8       = (1 << 32),
    FU_STU8       = (1 << 33),
    FU_LDU9       = (1 << 34),
    FU_STU9       = (1 << 35),
    FU_LDU10       = (1 << 36),
    FU_STU10       = (1 << 37),
    FU_LDU11       = (1 << 38),
    FU_STU11       = (1 << 39),
    FU_ALU8       = (1 << 40),
    FU_FPU8       = (1 << 41),
    FU_ALU9       = (1 << 42),
    FU_FPU9       = (1 << 43),
    FU_ALU10       = (1 << 44),
    FU_FPU10       = (1 << 45),
    FU_ALU11       = (1 << 46),
    FU_FPU11       = (1 << 47),
    FU_LDU12       = (1 << 48),
    FU_STU12       = (1 << 49),
    FU_LDU13       = (1 << 50),
    FU_STU13       = (1 << 51),
    FU_LDU14       = (1 << 52),
    FU_STU14       = (1 << 53),
    FU_LDU15       = (1 << 54),
    FU_STU15       = (1 << 55),
    FU_ALU12       = (1 << 56),
    FU_FPU12       = (1 << 57),
    FU_ALU13       = (1 << 58),
    FU_FPU13       = (1 << 59),
    FU_ALU14       = (1 << 60),
    FU_FPU14       = (1 << 61),
    FU_ALU15       = (1 << 62),
    FU_FPU15       = (1 << 63),
  };

  extern const char* fu_names[FU_COUNT];

  //
  // Opcodes and properties
  //
#define ALU0 (FU_ALU0 * ((ALU_FU_COUNT - 1) >= 0))
#define ALU1 (FU_ALU1 * ((ALU_FU_COUNT - 2) >= 0))
#define ALU2 (FU_ALU2 * ((ALU_FU_COUNT - 3) >= 0))
#define ALU3 (FU_ALU3 * ((ALU_FU_COUNT - 4) >= 0))
#define ALU4 (FU_ALU4 * ((ALU_FU_COUNT - 5) >= 0))
#define ALU5 (FU_ALU5 * ((ALU_FU_COUNT - 6) >= 0))
#define ALU6 (FU_ALU6 * ((ALU_FU_COUNT - 7) >= 0))
#define ALU7 (FU_ALU7 * ((ALU_FU_COUNT - 8) >= 0))
#define ALU8 (FU_ALU8 * ((ALU_FU_COUNT - 9) >= 0))
#define ALU9 (FU_ALU9 * ((ALU_FU_COUNT - 10) >= 0))
#define ALU10 (FU_ALU10 * ((ALU_FU_COUNT - 11) >= 0))
#define ALU11 (FU_ALU11 * ((ALU_FU_COUNT - 12) >= 0))
#define ALU12 (FU_ALU12 * ((ALU_FU_COUNT - 13) >= 0))
#define ALU13 (FU_ALU13 * ((ALU_FU_COUNT - 14) >= 0))
#define ALU14 (FU_ALU14 * ((ALU_FU_COUNT - 15) >= 0))
#define ALU15 (FU_ALU15 * ((ALU_FU_COUNT - 16) >= 0))

#define FPU0 (FU_FPU0 * ((FPU_FU_COUNT - 1) >= 0))
#define FPU1 (FU_FPU1 * ((FPU_FU_COUNT - 2) >= 0))
#define FPU2 (FU_FPU2 * ((FPU_FU_COUNT - 3) >= 0))
#define FPU3 (FU_FPU3 * ((FPU_FU_COUNT - 4) >= 0))
#define FPU4 (FU_FPU4 * ((FPU_FU_COUNT - 5) >= 0))
#define FPU5 (FU_FPU5 * ((FPU_FU_COUNT - 6) >= 0))
#define FPU6 (FU_FPU6 * ((FPU_FU_COUNT - 7) >= 0))
#define FPU7 (FU_FPU7 * ((FPU_FU_COUNT - 8) >= 0))
#define FPU8 (FU_FPU8 * ((FPU_FU_COUNT - 9) >= 0))
#define FPU9 (FU_FPU9 * ((FPU_FU_COUNT - 10) >= 0))
#define FPU10 (FU_FPU10 * ((FPU_FU_COUNT - 11) >= 0))
#define FPU11 (FU_FPU11 * ((FPU_FU_COUNT - 12) >= 0))
#define FPU12 (FU_FPU12 * ((FPU_FU_COUNT - 13) >= 0))
#define FPU13 (FU_FPU13 * ((FPU_FU_COUNT - 14) >= 0))
#define FPU14 (FU_FPU14 * ((FPU_FU_COUNT - 15) >= 0))
#define FPU15 (FU_FPU15 * ((FPU_FU_COUNT - 16) >= 0))

#define STU0 (FU_STU0 * ((STORE_FU_COUNT - 1) >= 0))
#define STU1 (FU_STU1 * ((STORE_FU_COUNT - 2) >= 0))
#define STU2 (FU_STU2 * ((STORE_FU_COUNT - 3) >= 0))
#define STU3 (FU_STU3 * ((STORE_FU_COUNT - 4) >= 0))
#define STU4 (FU_STU4 * ((STORE_FU_COUNT - 5) >= 0))
#define STU5 (FU_STU5 * ((STORE_FU_COUNT - 6) >= 0))
#define STU6 (FU_STU6 * ((STORE_FU_COUNT - 7) >= 0))
#define STU7 (FU_STU7 * ((STORE_FU_COUNT - 8) >= 0))
#define STU8 (FU_STU8 * ((STORE_FU_COUNT - 9) >= 0))
#define STU9 (FU_STU9 * ((STORE_FU_COUNT - 10) >= 0))
#define STU10 (FU_STU10 * ((STORE_FU_COUNT - 11) >= 0))
#define STU11 (FU_STU11 * ((STORE_FU_COUNT - 12) >= 0))
#define STU12 (FU_STU12 * ((STORE_FU_COUNT - 13) >= 0))
#define STU13 (FU_STU13 * ((STORE_FU_COUNT - 14) >= 0))
#define STU14 (FU_STU14 * ((STORE_FU_COUNT - 15) >= 0))
#define STU15 (FU_STU15 * ((STORE_FU_COUNT - 16) >= 0))

#define LDU0 (FU_LDU0 * ((LOAD_FU_COUNT - 1) >= 0))
#define LDU1 (FU_LDU1 * ((LOAD_FU_COUNT - 2) >= 0))
#define LDU2 (FU_LDU2 * ((LOAD_FU_COUNT - 3) >= 0))
#define LDU3 (FU_LDU3 * ((LOAD_FU_COUNT - 4) >= 0))
#define LDU4 (FU_LDU4 * ((LOAD_FU_COUNT - 5) >= 0))
#define LDU5 (FU_LDU5 * ((LOAD_FU_COUNT - 6) >= 0))
#define LDU6 (FU_LDU6 * ((LOAD_FU_COUNT - 7) >= 0))
#define LDU7 (FU_LDU7 * ((LOAD_FU_COUNT - 8) >= 0))
#define LDU8 (FU_LDU8 * ((LOAD_FU_COUNT - 9) >= 0))
#define LDU9 (FU_LDU9 * ((LOAD_FU_COUNT - 10) >= 0))
#define LDU10 (FU_LDU10 * ((LOAD_FU_COUNT - 11) >= 0))
#define LDU11 (FU_LDU11 * ((LOAD_FU_COUNT - 12) >= 0))
#define LDU12 (FU_LDU12 * ((LOAD_FU_COUNT - 13) >= 0))
#define LDU13 (FU_LDU13 * ((LOAD_FU_COUNT - 14) >= 0))
#define LDU14 (FU_LDU14 * ((LOAD_FU_COUNT - 15) >= 0))
#define LDU15 (FU_LDU15 * ((LOAD_FU_COUNT - 16) >= 0))

#define A ALULAT
#define L LOADLAT

//#define ANYALU ALU0|ALU1|ALU2|ALU3
#define ANYALU ALU0|ALU1|ALU2|ALU3|ALU4|ALU5|ALU6|ALU7|ALU8|ALU9|ALU10|ALU11|ALU12|ALU13|ALU14|ALU15
//#define ANYLDU LDU0|LDU1|LDU2|LDU3
#define ANYLDU LDU0|LDU1|LDU2|LDU3|LDU4|LDU5|LDU6|LDU7|LDU8|LDU9|LDU10|LDU11|LDU12|LDU13|LDU14|LDU15
//#define ANYSTU STU0|STU1|STU2|STU3
#define ANYSTU STU0|STU1|STU2|STU3|STU4|STU5|STU6|STU7|STU8|STU9|STU10|STU11|STU12|STU13|STU14|STU15
//#define ANYFPU FPU0|FPU1|FPU2|FPU3
#define ANYFPU FPU0|FPU1|FPU2|FPU3|FPU4|FPU5|FPU6|FPU7|FPU8|FPU9|FPU10|FPU11|FPU12|FPU13|FPU14|FPU15
#define ANYINT ANYALU|ANYSTU|ANYLDU
#define ALLFU  ANYINT|ANYFPU

//#define MAGICFU bitmask(FU_COUNT)

  struct FunctionalUnitInfo {
    byte opcode;   // Must match definition in ptlhwdef.h and ptlhwdef.cpp!
    byte latency;  // Latency in cycles, assuming ideal bypass
    //W16  fu;       // Map of functional units on which this uop can issue
    W64  fu;       // Map of functional units on which this uop can issue
  };

  //
  // WARNING: This table MUST be kept in sync with the table
  // in ptlhwdef.cpp and the uop enum in ptlhwdef.h!
  //
  const FunctionalUnitInfo fuinfo[OP_MAX_OPCODE] = {
    // name, latency, fumask
    {OP_nop,            A, ALLFU},
	//MAGICFU},
    {OP_mov,            A, ALLFU},
    // Logical
    {OP_and,            A, ALLFU},
    {OP_andnot,         A, ALLFU},
    {OP_xor,            A, ALLFU},
    {OP_or,             A, ALLFU},
    {OP_nand,           A, ALLFU},
    {OP_ornot,          A, ALLFU},
    {OP_eqv,            A, ALLFU},
    {OP_nor,            A, ALLFU},
    // Mask, insert or extract bytes
    {OP_maskb,          A, //ANYINT},
	ALLFU},
    // Add and subtract
    {OP_add,            A, //ANYINT},
	ALLFU},
    {OP_sub,            A, //ANYINT},
	ALLFU},
    {OP_adda,           A, //ANYINT},
	ALLFU},
    {OP_suba,           A, //ANYINT},
	ALLFU},
    {OP_addm,           A, //ANYINT},
	ALLFU},
    {OP_subm,           A, //ANYINT},
	ALLFU},
    // Condition code logical ops
    {OP_andcc,          A, //ANYINT},
	ALLFU},
    {OP_orcc,           A, //ANYINT},
	ALLFU},
    {OP_xorcc,          A, //ANYINT},
	ALLFU},
    {OP_ornotcc,        A, //ANYINT},
	ALLFU},
    // Condition code movement and merging
    {OP_movccr,         A, //ANYINT},
	ALLFU},
    {OP_movrcc,         A, //ANYINT},
	ALLFU},
    {OP_collcc,         A, //ANYINT},
	ALLFU},
    // Simple shifting (restricted to small immediate 1..8)
    {OP_shls,           A, //ANYINT},
	ALLFU},
    {OP_shrs,           A, //ANYINT},
	ALLFU},
    {OP_bswap,          A, //ANYINT},
	ALLFU},
    {OP_sars,           A, //ANYINT},
	ALLFU},
    // Bit testing
    {OP_bt,             A, //ANYALU},
	ALLFU},
    {OP_bts,            A, //ANYALU},
	ALLFU},
    {OP_btr,            A, //ANYALU},
	ALLFU},
    {OP_btc,            A, //ANYALU},
	ALLFU},
    // Set and select
    {OP_set,            A, //ANYINT},
	ALLFU},
    {OP_set_sub,        A, //ANYINT},
	ALLFU},
    {OP_set_and,        A, //ANYINT},
	ALLFU},
    {OP_sel,            A, //ANYINT},
	ALLFU},
    {OP_sel_cmp,        A, //ANYINT},
	ALLFU},
    // Branches
    {OP_br,             A, //ANYINT},
	ALLFU},
    {OP_br_sub,         A, //ANYINT},
	ALLFU},
    {OP_br_and,         A, //ANYINT},
	ALLFU},
    {OP_jmp,            A, //ANYINT},
	ALLFU},
    {OP_bru,            A, //ANYINT},
	ALLFU},
    {OP_jmpp,           A, //ANYALU|ANYLDU},
	ALLFU},
    {OP_brp,            A, //ANYALU|ANYLDU},
	ALLFU},
    // Checks
    {OP_chk,            A, //ANYINT},
	ALLFU},
    {OP_chk_sub,        A, //ANYINT},
	ALLFU},
    {OP_chk_and,        A, //ANYINT},
	ALLFU},
    // Loads and stores
    {OP_ld,             L, //ANYLDU},
	ALLFU},
    {OP_ldx,            L, //ANYLDU},
	ALLFU},
    {OP_ld_pre,         1, //ANYLDU},
	ALLFU},
    {OP_st,             1, //ANYSTU},
	ALLFU},
    {OP_mf,             1, //STU0  },
	ALLFU},
    // Shifts, rotates and complex masking
    {OP_shl,            A, //ANYALU},
	ALLFU},
    {OP_shr,            A, //ANYALU},
	ALLFU},
    {OP_mask,           A, //ANYALU},
	ALLFU},
    {OP_sar,            A, //ANYALU},
	ALLFU},
    {OP_rotl,           A, //ANYALU},
	ALLFU},
    {OP_rotr,           A, //ANYALU},
	ALLFU},
    {OP_rotcl,          A, //ANYALU},
	ALLFU},
    {OP_rotcr,          A, //ANYALU},
	ALLFU},
    // Multiplication
    {OP_mull,           4, //ANYFPU},
	ALLFU},
    {OP_mulh,           4, //ANYFPU},
	ALLFU},
    {OP_mulhu,          4, //ANYFPU},
	ALLFU},
    {OP_mulhl,          4, //ANYFPU},
	ALLFU},
    // Bit scans
    {OP_ctz,            3, //ANYFPU},
	ALLFU},
    {OP_clz,            3, //ANYFPU},
	ALLFU},
    {OP_ctpop,          3, //ANYFPU},
	ALLFU},
    {OP_permb,          4, //ANYFPU},
	ALLFU},
    // Integer divide and remainder step
    {OP_div,           32, //ALU0},
	ALLFU},
    {OP_rem,           32, //ALU0},
	ALLFU},
    {OP_divs,          32, //ALU0},
	ALLFU},
    {OP_rems,          32, //ALU0},
	ALLFU},
    // Minimum and maximum
    {OP_min,            A, //ANYALU},
	ALLFU},
    {OP_max,            A, //ANYALU},
	ALLFU},
    {OP_min_s,          A, //ANYALU},
	ALLFU},
    {OP_max_s,          A, //ANYALU},
	ALLFU},
    // Floating point
    // uop.size bits have following meaning:
    // 00 = single precision, scalar (preserve high 32 bits of ra)
    // 01 = single precision, packed (two 32-bit floats)
    // 1x = double precision, scalar or packed (use two uops to process 128-bit xmm)
    {OP_fadd,           6, //ANYFPU},
	ALLFU},
    {OP_fsub,           6, //ANYFPU},
	ALLFU},
    {OP_fmul,           6, //ANYFPU},
	ALLFU},
    {OP_fmadd,          6, //ANYFPU},
	ALLFU},
    {OP_fmsub,          6, //ANYFPU},
	ALLFU},
    {OP_fmsubr,         6, //ANYFPU},
	ALLFU},
    {OP_fdiv,           6, //ANYFPU},
	ALLFU},
    {OP_fsqrt,          6, //ANYFPU},
	ALLFU},
    {OP_frcp,           6, //ANYFPU},
	ALLFU},
    {OP_frsqrt,         6, //ANYFPU},
	ALLFU},
    {OP_fmin,           6, //ANYFPU},
	ALLFU},
    {OP_fmax,           6, //ANYFPU},
	ALLFU},
    {OP_fcmp,           6, //ANYFPU},
	ALLFU},
    // For fcmpcc, uop.size bits have following meaning:
    // 00 = single precision ordered compare
    // 01 = single precision unordered compare
    // 10 = double precision ordered compare
    // 11 = double precision unordered compare
    {OP_fcmpcc,         4, //ANYFPU},
	ALLFU},
    // and/andn/or/xor are done using integer uops
    // For these conversions, uop.size bits select truncation mode:
    // x0 = normal IEEE-style rounding
    // x1 = truncate to zero
    {OP_fcvt_i2s_ins,   6, //ANYFPU},
	ALLFU},
    {OP_fcvt_i2s_p,     6, //ANYFPU},
	ALLFU},
    {OP_fcvt_i2d_lo,    6, //ANYFPU},
	ALLFU},
    {OP_fcvt_i2d_hi,    6, //ANYFPU},
	ALLFU},
    {OP_fcvt_q2s_ins,   6, //ANYFPU},
	ALLFU},
    {OP_fcvt_q2d,       6, //ANYFPU},
	ALLFU},
    {OP_fcvt_s2i,       6, //ANYFPU},
	ALLFU},
    {OP_fcvt_s2q,       6, //ANYFPU},
	ALLFU},
    {OP_fcvt_s2i_p,     6, //ANYFPU},
	ALLFU},
    {OP_fcvt_d2i,       6, //ANYFPU},
	ALLFU},
    {OP_fcvt_d2q,       6, //ANYFPU},
	ALLFU},
    {OP_fcvt_d2i_p,     6, //ANYFPU},
	ALLFU},
    {OP_fcvt_d2s_ins,   6, //ANYFPU},
	ALLFU},
    {OP_fcvt_d2s_p,     6, //ANYFPU},
	ALLFU},
    {OP_fcvt_s2d_lo,    6, //ANYFPU},
	ALLFU},
    {OP_fcvt_s2d_hi,    6, //ANYFPU},
	ALLFU},
    // Vector integer uops
    // uop.size defines element size: 00 = byte, 01 = W16, 10 = W32, 11 = W64 (i.e. same as normal ALU uops)
    {OP_vadd,           1, //ANYFPU},
	ALLFU},
    {OP_vsub,           1, //ANYFPU},
	ALLFU},
    {OP_vadd_us,        1, //ANYFPU},
	ALLFU},
    {OP_vsub_us,        1, //ANYFPU},
	ALLFU},
    {OP_vadd_ss,        1, //ANYFPU},
	ALLFU},
    {OP_vsub_ss,        1, //ANYFPU},
	ALLFU},
    {OP_vshl,           1, //ANYFPU},
	ALLFU},
    {OP_vshr,           1, //ANYFPU},
	ALLFU},
    {OP_vbt,            1, //ANYFPU},
	ALLFU},
    {OP_vsar,           1, //ANYFPU},
	ALLFU},
    {OP_vavg,           1, //ANYFPU},
	ALLFU},
    {OP_vcmp,           1, //ANYFPU},
	ALLFU},
    {OP_vmin,           1, //ANYFPU},
	ALLFU},
    {OP_vmax,           1, //ANYFPU},
	ALLFU},
    {OP_vmin_s,         1, //ANYFPU},
	ALLFU},
    {OP_vmax_s,         1, //ANYFPU},
	ALLFU},
    {OP_vmull,          4, //ANYFPU},
	ALLFU},
    {OP_vmulh,          4, //ANYFPU},
	ALLFU},
    {OP_vmulhu,         4, //ANYFPU},
	ALLFU},
    {OP_vmaddp,         4, //ANYFPU},
	ALLFU},
    {OP_vsad,           4, //ANYFPU},
	ALLFU},
    {OP_vpack_us,       2, //ANYFPU},
	ALLFU},
    {OP_vpack_ss,       2, //ANYFPU},
	ALLFU},
    // Special Opcodes
    {OP_ast,			4, //ANYINT},
	ALLFU},
  };

#undef A
#undef L
#undef F

  struct OooCore;
  OooCore& coreof(W8 coreid);

  struct ReorderBufferEntry;

  //
  // Issue queue based scheduler with broadcast
  //
#ifdef BIG_ROB
  typedef W16 issueq_tag_t;
#else
  typedef byte issueq_tag_t;
#endif

  template <int size, int operandcount = MAX_OPERANDS>
  struct IssueQueue {
#ifdef BIG_ROB
    typedef FullyAssociativeTags16bit<size, size> assoc_t;
    typedef vec8w vec_t;
#else
    typedef FullyAssociativeTags8bit<size, size> assoc_t;
    typedef vec16b vec_t;
#endif

    typedef issueq_tag_t tag_t;

    static const int SIZE = size;

    assoc_t uopids;
    assoc_t tags[operandcount];

    // States:
    //             V I
    // free        0 0
    // dispatched  1 0
    // issued      1 1
    // complete    0 1

    bitvec<size> valid;
    bitvec<size> issued;
    bitvec<size> allready;
    int count;
    byte coreid;
    OooCore* core;
    int shared_free_entries;
    int reserved_entries;
    int issueq_id;
    static int issueq_id_seq;

    IssueQueue(){
      issueq_id = issueq_id_seq++;
    }
    void set_reserved_entries(int num) { reserved_entries = num; }
    bool reset_shared_entries() {
      shared_free_entries = size - reserved_entries;
      return true;
    }
    bool alloc_shared_entry() {
      assert(shared_free_entries > 0);
      shared_free_entries--;
      return true;
    }
    bool free_shared_entry() {
      if(logable(99)) ptl_logfile << "shared_free_entries: ", shared_free_entries, " size: ",  size, " reserved_entries: ",  reserved_entries, endl;
      assert(shared_free_entries < size - reserved_entries);
      shared_free_entries++;
      return true;
    }
    bool shared_empty() {
      return (shared_free_entries == 0);
    }

    bool remaining() const { return (size - count); }
    bool empty() const { return (!count); }
    bool full() const { return (!remaining()); }

    int uopof(int slot) const {
      return uopids[slot];
    }

    int slotof(int uopid) const {
      return uopids.search(uopid);
    }

    void reset(W8 coreid, OooCore* core);
    void reset(W8 coreid, W8 threadid, OooCore* core);
    void clock();
    bool insert(tag_t uopid, const tag_t* operands, const tag_t* preready);
    bool broadcast(tag_t uopid);
    int issue(int previd = -1);
    bool replay(int slot, const tag_t* operands, const tag_t* preready);
    bool switch_to_end(int slot, const tag_t* operands, const tag_t* preready);
    bool remove(int slot);

    ostream& print(ostream& os) const;
    void tally_broadcast_matches(tag_t sourceid, const bitvec<size>& mask, int operand);

    //
    // Replay a uop that has already issued once.
    // The caller may add or reset dependencies here as needed.
    //
    bool replay(int slot) {
      issued[slot] = 0;
      return true;
    }

    //
    // Remove an entry from the issue queue after it has completed,
    // or in the process of annulment.
    //
    bool release(int slot) {
      remove(slot);
      return true;
    }

    bool annul(int slot) {
      remove(slot);
      return true;
    }

    bool annuluop(int uopid) {
      int slot = slotof(uopid);
      if (slot < 0) return false;
      remove(slot);
      return true;
    }

    OooCore& getcore() { return *core; }
  };

  template <int size, int operandcount>
  static inline ostream& operator <<(ostream& os, const IssueQueue<size, operandcount>& issueq) {
    return issueq.print(os);
  }

  template <typename T>
  static void print_list_of_state_lists(ostream& os, const ListOfStateLists& lol, const char* title);

  //
  // Fetch Buffers
  //
  struct BranchPredictorUpdateInfo: public PredictorUpdate {
    int stack_recover_idx;
    int bptype;
    W64 ripafter;
  };


  struct DebugAddr{
    W64 virtaddr;
    W8 bytemask_1;
    W8 bytemask_2;
    W8 bytemask;
    W64 temp_data_1;
    W64 temp_data_2;
    W64 temp_data_3;
    bool type1;
    bool type2;
    bool type3;
    bool unaligned;
    bool pagefault;

    DebugAddr(){ 
      virtaddr = 0;
      bytemask_1 = 0; 
      bytemask_2 = 0; bytemask = 0; 
      temp_data_1 = 0; temp_data_2 = 0; temp_data_3 = 0;
      type1 = false; type2 = false; type3 = false;
      unaligned = false; pagefault = false; 
    }
  };

  struct FetchBufferEntry: public TransOp {
    //    friend std::ostream &operator <<(std::ostream &c, const FetchBufferEntry &T);
    //    friend std::ostream &operator <<(std::ostream &c, const FetchBufferEntry *pT);
    RIPVirtPhys rip;
    W64 uuid;
    uopimpl_func_t synthop;
    BranchPredictorUpdateInfo predinfo;
    W16 index;
    W8 threadid;
    byte ld_st_truly_unaligned;
    
    //
    W64 fake_result;
    W64 radata;
    W64 rbdata;
    W64 rcdata;
    W64 temp_radata;
    W64 temp_rbdata;
    W64 temp_rcdata;
    W64 virtaddr;
    bool perfbranchpred_touch;
    bool pagefault;

    DebugAddr dbgmsg;

    int init(int index) { this->index = index; perfbranchpred_touch = false; fake_result = 0; virtaddr = 0; pagefault = false; return 0;}
    void validate() {perfbranchpred_touch = false; fake_result = 0; virtaddr = 0; pagefault = false;}

    FetchBufferEntry() { perfbranchpred_touch = false; fake_result = 0; virtaddr = 0;  pagefault = false; }

    FetchBufferEntry(const TransOp& transop) {
      *((TransOp*)this) = transop;
      this->perfbranchpred_touch = false;
      this->fake_result = 0;
      this->virtaddr = 0;
      this->pagefault = false;
    }
  };

  //
  // ReorderBufferEntry
  struct ThreadContext;
  struct OooCore;
  struct PhysicalRegister;
  struct LoadStoreQueueEntry;

  //
  // Reorder Buffer (ROB) structure, used for tracking all uops in flight.
  // This same structure is used to represent both dispatched but not yet issued
  // uops as well as issued uops.
  //
  struct ReorderBufferEntry: public selfqueuelink {
    FetchBufferEntry uop;
    struct StateList* current_state_list;
    PhysicalRegister* physreg;
    PhysicalRegister* operands[MAX_OPERANDS];
    LoadStoreQueueEntry* lsq;
    W16s idx;
    W16s cycles_left; // execution latency counter, decremented every cycle when executing
    W16s forward_cycle; // forwarding cycle after completion
    W16s lfrqslot;
    W16s iqslot;
    W16  executable_on_cluster_mask;
    W8s  cluster;
    W8   coreid;
    OooCore* core;
    W64  tlb_miss_init_cycle;

    W8   threadid;
    byte fu;
    byte consumer_count;
    PTEUpdate pteupdate;
    Waddr origvirt; // original virtual address, with low bits
    Waddr virtpage; // virtual page number actually accessed by the load or store
    W64 original_addr, generated_addr, cache_data;
    byte entry_valid:1, load_store_second_phase:1, all_consumers_off_bypass:1, dest_renamed_before_writeback:1, no_branches_between_renamings:1, transient:1, lock_acquired:1, issued:1;
    byte annul_flag;
    byte tlb_walk_level;

    int index() const { return idx; }
    void validate() { entry_valid = true; }

    void changestate(StateList& newqueue, bool place_at_head = false, ReorderBufferEntry* prevrob = NULL) {
      if (current_state_list)
		current_state_list->remove(this);
      current_state_list = &newqueue;
      if (place_at_head) newqueue.enqueue_after(this, prevrob); else newqueue.enqueue(this);
    }

    void init(int idx);
    void reset();
    bool ready_to_issue() const;
    bool ready_to_commit() const;
    StateList& get_ready_to_issue_list();
    bool find_sources();
    int forward();
    int select_cluster();
    int issue();
    Waddr addrgen(LoadStoreQueueEntry& state, Waddr& origaddr, Waddr& virtpage, W64 ra, W64 rb, W64 rc, PTEUpdate& pteupdate, Waddr& addr, int& exception, PageFaultErrorCode& pfec, bool& annul);
    bool handle_common_load_store_exceptions(LoadStoreQueueEntry& state, Waddr& origaddr, Waddr& addr, int& exception, PageFaultErrorCode& pfec);
    int issuestore(LoadStoreQueueEntry& state, Waddr& origvirt, W64 ra, W64 rb, W64 rc, bool rcready, PTEUpdate& pteupdate);
    int issueload(LoadStoreQueueEntry& state, Waddr& origvirt, W64 ra, W64 rb, W64 rc, PTEUpdate& pteupdate);
    W64 get_load_data(LoadStoreQueueEntry& state, W64 data);
    void issueprefetch(IssueState& state, W64 ra, W64 rb, W64 rc, int cachelevel);
    void issueast(IssueState& state, W64 assistid, W64 ra, W64 rb, W64 rc, W16 raflags, W16 rbflags, W16 rcflags);
    int probecache(Waddr addr, LoadStoreQueueEntry* sfra);
    bool probetlb(LoadStoreQueueEntry& state, Waddr& origaddr, W64 ra, W64 rb, W64 rc, PTEUpdate& pteupdate);
    void tlbwalk();
    int issuefence(LoadStoreQueueEntry& state);
    void release();
    W64 annul(bool keep_misspec_uop, bool return_first_annulled_rip = false);
    W64 annul_after() { return annul(true); }
    W64 annul_after_and_including() { return annul(false); }
    int commit();
    void replay();
    void replay_locked();
    int pseudocommit();
    void redispatch(const bitvec<MAX_OPERANDS>& dependent_operands, ReorderBufferEntry* prevrob);
    void redispatch_dependents(bool inclusive = true);
    void loadwakeup();
    void fencewakeup();
    LoadStoreQueueEntry* find_nearest_memory_fence();
    bool release_mem_lock(bool forced = false);
    bool recheck_page_fault();
    ostream& print(ostream& os) const;
    stringbuf& get_operand_info(stringbuf& sb, int operand) const;
    ostream& print_operand_info(ostream& os, int operand);

    OooCore& getcore() const { return *core; }

    ThreadContext& getthread() const;
    issueq_tag_t get_tag();
  };

  static inline ostream& operator <<(ostream& os, const ReorderBufferEntry& rob) {
    return rob.print(os);
  }

  //
  // Load/Store Queue
  //
#define LSQ_SIZE (LDQ_SIZE + STQ_SIZE)

  // Define this to allow speculative issue of loads before unresolved stores
  //#define SMT_ENABLE_LOAD_HOISTING

  struct LoadStoreQueueEntry: public SFR {
    ReorderBufferEntry* rob;
    W16 idx;
    byte coreid;
    OooCore* core;
    W8s mbtag;
    W8 store:1, lfence:1, sfence:1, entry_valid:1, mmio:1;
    //   W32 padding;
    W32 time_stamp;
    W64 sfr_data;
    W8 sfr_bytemask;
    LoadStoreQueueEntry() { }

    int index() const { return idx; }

    void reset() {
      // int oldidx = idx;
      // setzero(*this);
      rob = 0;
      store = 0; lfence = 0; sfence = 0; entry_valid = 0;
      time_stamp = 0;
      // idx = oldidx;
      mbtag = -1;
      sfr_data = -1;
      sfr_bytemask = 0;
      mmio = 0;
    }

    void init(int idx) {
      this->idx = idx;
      reset();
    }

    void validate() { entry_valid = 1; }

    ostream& print(ostream& os) const;

    LoadStoreQueueEntry& operator =(const SFR& sfr) {
      *((SFR*)this) = sfr;
      return *this;
    }

    OooCore& getcore() { return *core; }
  };

  static inline ostream& operator <<(ostream& os, const LoadStoreQueueEntry& lsq) {
    return lsq.print(os);
  }

  struct PhysicalRegisterOperandInfo {
    W32 uuid;
    W16 physreg;
    W16 rob;
    byte state;
    byte rfid;
    byte archreg;
    byte pad1;
  };

  ostream& operator <<(ostream& os, const PhysicalRegisterOperandInfo& opinfo);

  //
  // Physical Register File
  //

  struct PhysicalRegister: public selfqueuelink {
    ReorderBufferEntry* rob;
    W64 data;
    W16 flags;
    W16 idx;
    W8  coreid;
    OooCore* core;
    W8  rfid;
    W8  state;
    W8  archreg;
    W8  all_consumers_sourced_from_bypass:1;
    W16s refcount;
    W8 threadid;

    StateList& get_state_list(int state) const;
    StateList& get_state_list() const { return get_state_list(this->state); }

    void changestate(int newstate) {
      if likely (state != PHYSREG_NONE) get_state_list(state).remove(this);
      state = newstate;
      get_state_list(state).enqueue(this);
    }

    void init(W8 coreid, int rfid, int idx, OooCore* core) {
      this->coreid = coreid;
      this->core = core;
      this->rfid = rfid;
      this->idx = idx;
      reset();
    }

  private:
    void addref() { refcount++; }
    void unref() {
      refcount--;
      assert((idx == 0) || (refcount >= 0));
    }

  public:

    void addref(const ReorderBufferEntry& rob, W8 threadid) { addref(); }
    void unref(const ReorderBufferEntry& rob, W8 threadid) { unref(); }
    void addspecref(int archreg, W8 threadid) { addref(); }
    void unspecref(int archreg, W8 threadid) { unref(); }
    void addcommitref(int archreg, W8 threadid) { addref(); }
    void uncommitref(int archreg, W8 threadid) { unref();  }

    bool referenced() const { return (refcount > 0); }
    bool nonnull() const { return (index() != PHYS_REG_NULL); }
    bool allocated() const { return (state != PHYSREG_FREE); }
    void commit() { changestate(PHYSREG_ARCH); }
    void complete() { changestate(PHYSREG_BYPASS); }
    void writeback() { changestate(PHYSREG_WRITTEN); }

    void free() {
      changestate(PHYSREG_FREE);
      rob = 0;
      refcount = 0;
      threadid = 0xff;
      all_consumers_sourced_from_bypass = 1;
      flags = flags & ~(FLAG_INV | FLAG_WAIT);
    }

  private:
    void reset() {
      selfqueuelink::reset();
      state = PHYSREG_NONE;
      free();
    }

  public:
    void reset(W8 threadid, bool check_id = true) {
      if (check_id && this->threadid != threadid) return;

      if (!check_id) {
	selfqueuelink::reset();
	state = PHYSREG_NONE;
      }
      free();
    }

    int index() const { return idx; }
    bool valid() const { return ((flags & FLAG_INV) == 0); }
    bool ready() const { return ((flags & FLAG_WAIT) == 0); }

    void fill_operand_info(PhysicalRegisterOperandInfo& opinfo);

    OooCore& getcore() { return *core; }
  };

  ostream& operator <<(ostream& os, const PhysicalRegister& physreg);

  struct PhysicalRegisterFile: public array<PhysicalRegister, MAX_PHYS_REG_FILE_SIZE> {
    byte coreid;
    OooCore *core;
    byte rfid;
    W16 size;
    const char* name;
    StateList states[MAX_PHYSREG_STATE];
    W64 allocations;
    W64 frees;

    PhysicalRegisterFile() { }

    PhysicalRegisterFile(const char* name, W8 coreid, int rfid, int size,
			 OooCore* core) {
      init(name, coreid, rfid, size, core); reset();
    }

    PhysicalRegisterFile& operator ()(const char* name, W8 coreid, int rfid, int size, OooCore* core) {
      init(name, coreid, rfid, size, core); reset(); return *this;
    }

    bool cleanup();

    void init(const char* name, W8 coreid, int rfid, int size, OooCore* core);
    // bool remaining() const { return (!states[PHYSREG_FREE].empty()); }
    bool remaining() {
      if unlikely (states[PHYSREG_FREE].empty()) {
	  return cleanup();
	}
      return true;
    }

    PhysicalRegister* alloc(W8 threadid, int r = -1);
    void reset(W8 threadid);
    ostream& print(ostream& os) const;

    OooCore& getcore() { return *core; }

  private:
    void reset();

  };

  static inline ostream& operator <<(ostream& os, const PhysicalRegisterFile& physregs) {
    return physregs.print(os);
  }

  //
  // Register Rename Table
  //
  struct RegisterRenameTable: public array<PhysicalRegister*, TRANSREG_COUNT> {
#ifdef ENABLE_TRANSIENT_VALUE_TRACKING
    bitvec<TRANSREG_COUNT> renamed_in_this_basic_block;
#endif
    ostream& print(ostream& os) const;
  };

  static inline ostream& operator <<(ostream& os, const RegisterRenameTable& rrt) {
    return rrt.print(os);
  }

  enum {
    ISSUE_COMPLETED = 1,      // issued correctly
    ISSUE_NEEDS_REPLAY = 0,   // fast scheduling replay
    ISSUE_MISSPECULATED = -1, // mis-speculation: redispatch dependent slice
    ISSUE_NEEDS_REFETCH = -2, // refetch from RIP of bad insn
    ISSUE_SKIPPED = -3,        // used to indicate that skip this Issue (used for light assist)
  };

  enum {
    COMMIT_RESULT_NONE = 0,   // no instructions committed: some uops not ready
    COMMIT_RESULT_OK = 1,     // committed
    COMMIT_RESULT_EXCEPTION = 2, // exception
    COMMIT_RESULT_BARRIER = 3,// barrier; branch to microcode (brp uop)
    COMMIT_RESULT_SMC = 4,    // self modifying code detected
    COMMIT_RESULT_INTERRUPT = 5, // interrupt pending
    COMMIT_RESULT_STOP = 6    // stop processor model (shutdown)
  };

  // Branch predictor outcomes:
  enum { MISPRED = 0, CORRECT = 1 };

  //
  // Lookup tables (LUTs):
  //
  struct Cluster {
    const char* name;
    //W16 issue_width;
    W32 issue_width;
    //W32 fu_mask;
    W64 fu_mask;
  };

  extern const Cluster clusters[MAX_CLUSTERS];
  extern byte uop_executable_on_cluster[OP_MAX_OPCODE];
  extern W32 forward_at_cycle_lut[MAX_CLUSTERS][MAX_FORWARDING_LATENCY+1];
  extern const byte archdest_can_commit[TRANSREG_COUNT];
  extern const byte archdest_is_visible[TRANSREG_COUNT];
  extern bool globals_initialized;

  struct LoadStoreAliasPredictor: public FullyAssociativeTags<W64, 8> { };

  enum {
    ROB_STATE_READY = (1 << 0),
    ROB_STATE_IN_ISSUE_QUEUE = (1 << 1),
    ROB_STATE_PRE_READY_TO_DISPATCH = (1 << 2)
  };

#ifdef MULTI_IQ
#define InitClusteredROBList(name, description, flags)	\
  name[0](description "-int0", rob_states, flags);	\
  name[1](description "-int1", rob_states, flags);	\
  name[2](description "-ld", rob_states, flags);	\
  name[3](description "-fp", rob_states, flags)
#else
#define InitClusteredROBList(name, description, flags)	\
  name[0](description "-all", rob_states, flags);
#endif

  //
  // TLB class with one-hot semantics. 36 bit tags are required since
  // virtual addresses are 48 bits, so 48 - 12 (2^12 bytes per page)
  // is 36 bits.
  //
  template <int tlbid, int size>
  struct TranslationLookasideBuffer: public FullyAssociativeTagsNbitOneHot<size, 40> {
    typedef FullyAssociativeTagsNbitOneHot<size, 40> base_t;
    TranslationLookasideBuffer(): base_t() { }

    void reset() {
      base_t::reset();
    }

    // Get the 40-bit TLB tag (36 bit virtual page ID plus 4 bit threadid)
    static W64 tagof(W64 addr, W64 threadid) {
      return bits(addr, 12, 36) | (threadid << 36);
    }

    bool probe(W64 addr, W8 threadid = 0) {
      W64 tag = tagof(addr, threadid);
      return (base_t::probe(tag) >= 0);
    }

    bool insert(W64 addr, W8 threadid = 0) {
      addr = floor(addr, PAGE_SIZE);
      W64 tag = tagof(addr, threadid);
      W64 oldtag = 0;
      int way = base_t::select(tag, oldtag);
      if (logable(6)) {
	ptl_logfile << "TLB insertion of virt page ", (void*)(Waddr)addr, " (virt addr ",
	  (void*)(Waddr)(addr), ") into way ", way, ": ",
	  ((oldtag != tag) ? "evicted old entry" : "already present"), endl;
      }
      return (oldtag != tag);
    }

    int flush_all() {
      reset();
      return size;
    }

    int flush_thread(W64 threadid) {
      W64 tag = threadid << 36;
      W64 tagmask = 0xfULL << 36;
      bitvec<size> slotmask = base_t::masked_match(tag, tagmask);
      int n = slotmask.popcount();
      base_t::masked_invalidate(slotmask);
      return n;
    }

    int flush_virt(Waddr virtaddr, W64 threadid) {
      return invalidate(tagof(virtaddr, threadid));
    }
  };

  template <int tlbid, int size>
  static inline ostream& operator <<(ostream& os, const TranslationLookasideBuffer<tlbid, size>& tlb) {
    return tlb.print(os);
  }

  typedef TranslationLookasideBuffer<0, DTLB_SIZE> DTLB;
  typedef TranslationLookasideBuffer<1, ITLB_SIZE> ITLB;

  inline void sigsegv_handler(int signo){
    ptl_logfile.flush();
    raise(SIGINT);
  }


  struct PerfectBranchPredictor{
    struct physreg{
      W64 data;
      W16 flags;
      W8 bytemask;
      
      void reset() { data = 0; flags = 0xff; bytemask = 0xff; }
    };

    W64 mispredicted;
    W64 count;
    W64 try_count;
    W64 failed_count;
    W64 internal;
    W64 fence;
    W64 invalid;
    W64 ast;
    W64 pagefault;
    W64 matched;
    W64 notmatched;
    W64 miss_load;
    W64 miss_store;
    W64 miss_branch;
    W64 miss_other;
    W8 phys_ra;
    W8 phys_rb;
    W8 phys_rc;
    W64 ok_load;

    array<physreg, TRANSREG_COUNT> regfile;
    //write buffer
    typedef FullyAssociativeArray<W64, physreg, 2 * (LSQ_SIZE + FETCH_QUEUE_SIZE), 
				  NullAssociativeArrayStatisticsCollector<W64, physreg> > WBbuf;
    WBbuf wbbuf;
    WBbuf internal_wbbuf;

    ThreadContext *thread;
    PerfectBranchPredictor(ThreadContext *thread) {
      mispredicted = 0;
      count = 0;
      try_count = 0;
      failed_count = 0;
      fence = 0;
      internal = 0;
      invalid = 0;
      ast = 0;
      pagefault = 0;
      matched = 0;
      notmatched = 0;
      miss_load = 0;
      miss_store = 0;
      miss_other = 0;
      miss_branch = 0;
      ok_load = 0;
      signal(SIGSEGV,sigsegv_handler);
      this->thread = thread;
    }
    ~PerfectBranchPredictor(void){
      ptl_logfile << "MISS : " , mispredicted, endl,
	"BRANCH : ", count, endl,
	"TRY : ", try_count, endl,
	"FAIL : ", failed_count, endl,
	"FENCE : ", fence, endl,
	"INTERNAL : ", internal, endl,
	"INVALID : ", invalid, endl,
	"AST : ", ast, endl,
	"PAGEFAULT : ", pagefault, endl,
	"MATCHED : ", matched, endl,
	"LOAD : ", ok_load, endl,
	"NOT MATCHED : ", notmatched, endl,
	"LOAD : ", miss_load, endl,
	"STORE : ", miss_store, endl,
	"BRANCH : ", miss_branch, endl,
	"OTHER : ", miss_other, endl;
    }
    void setup(const RegisterRenameTable& rrt);
    W64 simple_addr(W64 ra, W64 rb);
    bool addrgen(Waddr &virtaddr, W64 ra, W64 rb, bool st,  int sizeshift);
    void executeLoad(IssueState &state, W64 radata, W64 rbdata, bool internal, W8 sizeshift, bool signext, DebugAddr &dbgmsg);
    void executeStore(IssueState &state, W64 radata, W64 rbdata, W64 rcdata, bool internal, W8 sizeshift, DebugAddr &dbgmsg);
    bool emulate(FetchBufferEntry& tr, W64 &predaddr);
    W64 predict(Queue<FetchBufferEntry, FETCH_QUEUE_SIZE> &fetchq,     
		Queue<ReorderBufferEntry, ROB_SIZE> &rob,
		RegisterRenameTable &rrt,
		bool &fail);
  };


  struct ThreadContext {
    OooCore& core;
    OooCore& getcore() { return core; }
    ThreadContext& getthread() { return *this; }

    PTLsimStats *stats_;

    W8 threadid;
    W8 coreid;
    Context& ctx;
    BranchPredictorInterface branchpred;
    PerfectBranchPredictor perfbranchpred;

    Queue<FetchBufferEntry, FETCH_QUEUE_SIZE> fetchq;

    ListOfStateLists rob_states;
    ListOfStateLists lsq_states;
    //
    // Each ROB's state can be linked into at most one of the
    // following rob_xxx_list lists at any given time; the ROB's
    // current_state_list points back to the list it belongs to.
    //
    StateList rob_free_list;                             // Free ROB entyry
    StateList rob_frontend_list;                         // Frontend in progress (artificial delay)
    StateList rob_ready_to_dispatch_list;                // Ready to dispatch
    StateList rob_dispatched_list[MAX_CLUSTERS];         // Dispatched but waiting for operands
    StateList rob_ready_to_issue_list[MAX_CLUSTERS];     // Ready to issue (all operands ready)
    StateList rob_ready_to_store_list[MAX_CLUSTERS];     // Ready to store (all operands except possibly rc are ready)
    StateList rob_ready_to_load_list[MAX_CLUSTERS];      // Ready to load (all operands ready)
    StateList rob_issued_list[MAX_CLUSTERS];             // Issued and in progress (or for loads, returned here after address is generated)
    StateList rob_completed_list[MAX_CLUSTERS];          // Completed and result in transit for local and global forwarding
    StateList rob_ready_to_writeback_list[MAX_CLUSTERS]; // Completed; result ready to writeback in parallel across all cluster register files
    StateList rob_cache_miss_list;                       // Loads only: wait for cache miss to be serviced
    StateList rob_tlb_miss_list;                         // TLB miss waiting to be serviced on one or more levels
    StateList rob_memory_fence_list;                     // mf uops only: wait for memory fence to reach head of LSQ before completing
    StateList rob_ready_to_commit_queue;                 // Ready to commit

    Queue<ReorderBufferEntry, ROB_SIZE> ROB;

    Queue<LoadStoreQueueEntry, LSQ_SIZE> LSQ;
    RegisterRenameTable specrrt;
    RegisterRenameTable commitrrt;

    DTLB dtlb;
    ITLB itlb;
    void setupTLB();
    W64 itlb_miss_init_cycle;
    bool in_tlb_walk;

    // Fetch-related structures
    RIPVirtPhys fetchrip;
    BasicBlock* current_basic_block;
    int current_basic_block_transop_index;
    bool stall_frontend;
    bool waiting_for_icache_fill;
    Waddr waiting_for_icache_fill_physaddr;
    byte itlb_walk_level;
    bool probeitlb(Waddr fetchrip);
    void itlbwalk();

    // Last block in icache we fetched into our buffer
    W64 current_icache_block;
    W64 fetch_uuid;
    int loads_in_flight;
    int stores_in_flight;
    bool prev_interrupts_pending;
    bool handle_interrupt_at_next_eom;
    bool stop_at_next_eom;

    W64 last_commit_at_cycle;
    bool smc_invalidate_pending;
    RIPVirtPhys smc_invalidate_rvp;
    W64 chk_recovery_rip;

    TransOpBuffer unaligned_ldst_buf;
    LoadStoreAliasPredictor lsap;
    int loads_in_this_cycle;
    W64 load_to_store_parallel_forwarding_buffer[LOAD_FU_COUNT];

    W64 consecutive_commits_inside_spinlock;
    W64 pause_counter;

    /***** by vteori *****/
    // for trace
    bool is_ibuf_miss;
    bool is_itlb_miss;
    bool is_l1_icache_miss;
    bool is_l2_icache_miss;
	bool is_icache_waiting;
    // for FMT
    bool is_flushed;
    // for tracking insufficient resources
    int physreg_idx;
    int lsq_full_idx;
    int ldq_full_idx;
    int stq_full_idx;

    // statistics:
    W64 total_uops_committed;
    W64 total_insns_committed;
    int dispatch_deadlock_countdown;
#ifdef MULTI_IQ
    int issueq_count[4]; // number of occupied issuequeue entries
#else
    int issueq_count;
#endif

    //
    // List of memory locks that will be removed from
    // the lock controller when the macro-op commits.
    //
    // At most 4 chunks are allowed, to ensure
    // cmpxchg16b works even with unaligned data.
    //
    byte queued_mem_lock_release_count;
    W64 queued_mem_lock_release_list[4];

    ThreadContext(OooCore& core_, W8 threadid_, Context& ctx_);

    int commit();
    int writeback(int cluster);
    int transfer(int cluster);
    int complete(int cluster);
    int dispatch();
    void frontend();
    void rename();
    bool fetch();
    void tlbwalk();

    void readycheck(); // (Trace) by vteori 

    bool handle_barrier();
    bool handle_exception();
    bool handle_interrupt();
    void reset_fetch_unit(W64 realrip);
    void flush_pipeline();
    void invalidate_smc();
    void external_to_core_state();
    void core_to_external_state() { }
    void annul_fetchq();
    BasicBlock* fetch_or_translate_basic_block(const RIPVirtPhys& rvp);
    void redispatch_deadlock_recovery();
    void flush_mem_lock_release_list(int start = 0);
    int get_priority() const;

    void dump_smt_state(ostream& os);
    void print_smt_state(ostream& os);
    void print_rob(ostream& os);
    void print_lsq(ostream& os);
    void print_rename_tables(ostream& os);

    void reset();
    void init();

    // Stats
    OooCoreThreadStats thread_stats;
    Interval& interval; // by vteori : interval analysis
    Interval& periodic_interval; // by vteori : interval analysis
  };

  //  class MemoryHierarchy;
  //


  // checkpointed core
  //
  struct OooCore: public BaseCore {
    W8 coreid;
    OooCore& getcore() { return *this; }

    /* This is only used for stats collection. By default if core is
     * collecting stats that is common across threads then its collected
     * into Stats that Thread-0 is using. */
    ThreadContext& getthread() { return *threads[0]; }

    PTLsimStats *stats_;

    int threadcount;
    ThreadContext** threads;

    ListOfStateLists rob_states;
    ListOfStateLists lsq_states;

    ListOfStateLists physreg_states;
    // Bandwidth counters:
    int commitcount;
    int writecount;
    int dispatchcount;
    int renamecount; // by vteori

    byte round_robin_tid;


    //
    // Issue Queues (one per cluster)
    //

#define declare_issueq_templates template struct IssueQueue<ISSUE_QUEUE_SIZE>
#ifdef MULTI_IQ
    IssueQueue<ISSUE_QUEUE_SIZE> issueq_int0;
    IssueQueue<ISSUE_QUEUE_SIZE> issueq_int1;
    IssueQueue<ISSUE_QUEUE_SIZE> issueq_ld;
    IssueQueue<ISSUE_QUEUE_SIZE> issueq_fp;

    int reserved_iq_entries[4];  /// this is the total number of iq entries reserved per thread.
    // Instantiate any issueq sizes used above:


#define foreach_issueq(expr) { OooCore& core = getcore(); core.issueq_int0.expr; core.issueq_int1.expr; core.issueq_ld.expr; core.issueq_fp.expr; }

    void sched_get_all_issueq_free_slots(int* a) {
      a[0] = issueq_int0.remaining();
      a[1] = issueq_int1.remaining();
      a[2] = issueq_ld.remaining();
      a[3] = issueq_fp.remaining();
    }

#define issueq_operation_on_cluster_with_result(core, cluster, rc, expr) \
    switch (cluster) {							\
    case 0: rc = core.issueq_int0.expr; break;				\
    case 1: rc = core.issueq_int1.expr; break;				\
    case 2: rc = core.issueq_ld.expr; break;				\
    case 3: rc = core.issueq_fp.expr; break;				\
    }

#define issueq_operation_on_cluster_no_res(core, cluster, expr) \
    switch (cluster) {						\
    case 0: core.issueq_int0.expr; break;			\
    case 1: core.issueq_int1.expr; break;			\
    case 2: core.issueq_ld.expr; break;				\
    case 3: core.issueq_fp.expr; break;				\
    }

#define per_cluster_stats_update(prefix, cluster, expr) \
    switch (cluster) {					\
    case 0: CORE_STATS(prefix.int0) expr; break;	\
    case 1: CORE_STATS(prefix.int1) expr; break;	\
    case 2: CORE_STATS(prefix.ld) expr; break;		\
    case 3: CORE_STATS(prefix.fp) expr; break;		\
    }

#else
    IssueQueue<ISSUE_QUEUE_SIZE> issueq_all;

    int reserved_iq_entries;  /// this is the total number of iq entries reserved per thread.

#define foreach_issueq(expr) { getcore().issueq_all.expr; }
    void sched_get_all_issueq_free_slots(int* a) {
      a[0] = issueq_all.remaining();
    }
#define issueq_operation_on_cluster_with_result(core, cluster, rc, expr) rc = core.issueq_all.expr;
#define issueq_operation_on_cluster_no_res(core, cluster, expr) core.issueq_all.expr;
#define per_cluster_stats_update(prefix, cluster, expr) CORE_STATS(prefix.all) expr;

#endif

#define per_physregfile_stats_update(prefix, rfid, expr)	\
    switch (rfid) {						\
    case 0: CORE_STATS(prefix.integer) expr; break;		\
    case 1: CORE_STATS(prefix.fp) expr; break;			\
    case 2: CORE_STATS(prefix.st) expr; break;			\
    case 3: CORE_STATS(prefix.br) expr; break;			\
    }

#define issueq_operation_on_cluster(core, cluster, expr) { issueq_operation_on_cluster_no_res(core, cluster, expr); }

#define for_each_cluster(iter) foreach (iter, MAX_CLUSTERS)
#define for_each_operand(iter) foreach (iter, MAX_OPERANDS)

    OooCore(BaseMachine& machine_, W8 num_threads, const char* name=NULL);

    ~OooCore(){
      foreach (i, threadcount) delete threads[i];
    };

    //
    // Initialize structures independent of the core parameters
    //
    void init_generic();
    void reset();

    //
    // Initialize all structures for the first time
    //
    void init() {
      init_generic();
      //
      // Physical register files
      //
#ifdef UNIFIED_PHYS_REG_FILE
      physregfiles[0]("all", coreid, 0, PHYS_REG_FILE_SIZE, this);
#else
#ifdef UNIFIED_INT_FP_PHYS_REG_FILE
      physregfiles[0]("int", coreid, 0, PHYS_REG_FILE_SIZE, this);
      physregfiles[1]("st", coreid, 1, STQ_SIZE * threadcount, this);
      physregfiles[2]("br", coreid, 2, MAX_BRANCHES_IN_FLIGHT * threadcount, this);
#else
      physregfiles[0]("int", coreid, 0, PHYS_REG_FILE_SIZE, this);
      physregfiles[1]("fp", coreid, 1, PHYS_REG_FILE_SIZE, this);
      physregfiles[2]("st", coreid, 2, STQ_SIZE * threadcount, this);
      physregfiles[3]("br", coreid, 3, MAX_BRANCHES_IN_FLIGHT * threadcount, this);
#endif
#endif
    }

    //
    // Physical Registers
    //

#ifdef UNIFIED_PHYS_REG_FILE
    enum { PHYS_REG_FILE_ALL };
#else
#ifdef UNIFIED_INT_FP_PHYS_REG_FILE
    enum { PHYS_REG_FILE_INT, PHYS_REG_FILE_ST, PHYS_REG_FILE_BR };
#else
    enum { PHYS_REG_FILE_INT, PHYS_REG_FILE_FP, PHYS_REG_FILE_ST, PHYS_REG_FILE_BR };
#endif
#endif

    enum {
#ifdef UNIFIED_PHYS_REG_FILE
      PHYS_REG_FILE_MASK_ALL  = (1 << 0)
#else
#ifdef UNIFIED_INT_FP_PHYS_REG_FILE
      PHYS_REG_FILE_MASK_INT = (1 << 0),
      PHYS_REG_FILE_MASK_ST  = (1 << 1),
      PHYS_REG_FILE_MASK_BR  = (1 << 2)
#else
      PHYS_REG_FILE_MASK_INT = (1 << 0),
      PHYS_REG_FILE_MASK_FP  = (1 << 1),
      PHYS_REG_FILE_MASK_ST  = (1 << 2),
      PHYS_REG_FILE_MASK_BR  = (1 << 3)
#endif
#endif
    };

    // Major core structures
    PhysicalRegisterFile physregfiles[PHYS_REG_FILE_COUNT];
    int round_robin_reg_file_offset;
    W32 fu_avail;
    ReorderBufferEntry* robs_on_fu[FU_COUNT];
    // CacheSubsystem::CacheHierarchy caches;
    // CPUControllerNamespace::CPUController cpu_controller;
    //    MemorySystem::CPUController test_controller;
    // OutOfOrderCoreCacheCallbacks cache_callbacks;

    // Unaligned load/store predictor
    bitvec<UNALIGNED_PREDICTOR_SIZE> unaligned_predictor;
    static int hash_unaligned_predictor_slot(const RIPVirtPhysBase& rvp);
    bool get_unaligned_hint(const RIPVirtPhysBase& rvp) const;
    void set_unaligned_hint(const RIPVirtPhysBase& rvp, bool value);

    // Pipeline Stages
    bool runcycle(void*);
    void flush_pipeline();
    bool fetch();
    void rename();
    void frontend();
    int dispatch();
    int issue(int cluster);
    int complete(int cluster);
    int transfer(int cluster);
    int writeback(int cluster);
    int commit();

    void flush_tlb(Context& ctx);
    void flush_tlb_virt(Context& ctx, Waddr virtaddr);

    // Cache Signals and Callbacks
    Signal dcache_signal;
    Signal icache_signal;
    Signal run_cycle;

    bool dcache_wakeup(void *arg);
    bool icache_wakeup(void *arg);

    // Debugging
    void dump_state(ostream& os);
    void print_smt_state(ostream& os);
    void check_refcounts();
    void check_rob();

    // Stats
    OooCoreStats core_stats;

    void update_stats();

    void check_ctx_changes();

    W8 get_coreid() { return coreid; }

    void dump_configuration(YAML::Emitter &out) const;
  };

  /* Checker - saved stores to compare after executing emulated instruction */
  struct CheckStores {
    W64 virtaddr;
    W64 data;
    W8 sizeshift;
    W8 bytemask;
  };

  extern CheckStores *checker_stores;
  extern int checker_stores_count;

  void reset_checker_stores();

  void add_checker_store(LoadStoreQueueEntry* lsq, W8 sizeshift);

  extern CycleTimer cttotal;
  extern CycleTimer ctfetch;
  extern CycleTimer ctdecode;
  extern CycleTimer ctrename;
  extern CycleTimer ctfrontend;
  extern CycleTimer ctdispatch;
  extern CycleTimer ctissue;
  extern CycleTimer ctissueload;
  extern CycleTimer ctissuestore;
  extern CycleTimer ctcomplete;
  extern CycleTimer cttransfer;
  extern CycleTimer ctwriteback;
  extern CycleTimer ctcommit;

#ifdef DECLARE_STRUCTURES
  //
  // The following configuration has two integer/store clusters with a single cycle
  // latency between them, but both clusters can access the load pseudo-cluster with
  // no extra cycle. The floating point cluster is two cycles from everything else.
  //
#ifdef MULTI_IQ
  const Cluster clusters[MAX_CLUSTERS] = {
    {"int0",  2, (FU_ALU0|FU_STU0)},
    {"int1",  2, (FU_ALU1|FU_STU1)},
    {"ld",    2, (FU_LDU0|FU_LDU1)},
    {"fp",    2, (FU_FPU0|FU_FPU1)},
  };

  const byte intercluster_latency_map[MAX_CLUSTERS][MAX_CLUSTERS] = {
    // I0 I1 LD FP <-to
    {0, 1, 0, 2}, // from I0
    {1, 0, 0, 2}, // from I1
    {0, 0, 0, 2}, // from LD
    {2, 2, 2, 0}, // from FP
  };

  const byte intercluster_bandwidth_map[MAX_CLUSTERS][MAX_CLUSTERS] = {
    // I0 I1 LD FP <-to
    {2, 2, 1, 1}, // from I0
    {2, 2, 1, 1}, // from I1
    {1, 1, 2, 2}, // from LD
    {1, 1, 1, 2}, // from FP
  };

#else // single issueq
  const Cluster clusters[MAX_CLUSTERS] = {
    //{"all",  4, (ALLFU)},
    {"all",  MAX_ISSUE_WIDTH, (ALLFU)},
  };
  const byte intercluster_latency_map[MAX_CLUSTERS][MAX_CLUSTERS] = {{0}};
  const byte intercluster_bandwidth_map[MAX_CLUSTERS][MAX_CLUSTERS] = {{64}};
#endif // multi_issueq

#endif // DECLARE_STRUCTURES

  struct OooCoreBuilder : public CoreBuilder {
    OooCoreBuilder(const char* name);
    BaseCore* get_new_core(BaseMachine& machine, const char* name);
  };
};

#undef ALU0
#undef ALU1
#undef ALU2
#undef ALU3

#undef FPU0
#undef FPU1
#undef FPU2
#undef FPU3

#undef STU0
#undef STU1
#undef STU2
#undef STU3

#undef LDU0
#undef LDU1
#undef LDU2
#undef LDU3

#undef ANYALU
#undef ANYLDU
#undef ANYSTU
#undef ANYFPU
#undef ANYINT
#undef ALLFU

#endif // _OOOCORE_H_

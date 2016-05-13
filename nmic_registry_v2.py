from RegisterEditor import *

class NmicRegistry():
    def __init__(self, parent=None):
        self.init__ = super().__init__()
        self.regs = [ Register(0x00, "CHIP_ID",    0X0000, [("CHIP_ID", 8),("CHIP_REV1",4),("CHIP_REV2",4)], self, True),
                      Register(0x01, "STATUS",     0x0000, [("STIM_ACTV",1),("",8),("ERR_POR",1),("ERR_CRC",1),("ERR_CFG",1),("ERR_COMP",4)], self, True),
                      Register(0x02, "PWR_CONFIG", 0x0000, [("HI_PWR_EN",1),("HV_CLKSHDN",1),("LV_CLKSEL",2),("HV_CLKSEL",3),("HV_TRI",1),("HV_DIS",1),("HV_VOLT",2),("FORCE_CP",1),("FORCE_LDO",1),("FORCE_POR3",1),("FORCE_POR1",1),("LV_RATIO",1)], self),
                      Register(0x03, "TEST_SEL",   0x0000, [("BG_SF_EN",1),("AN_SF_EN",1),("HV_SF_EN",1),("HV_TEST_SEL",2),("AN_TEST_SEL",2),("BG_TEST_SEL",3),("DTEST_SEL",6)], self),
                      Register(0x04, "REC_EN0",    0x0000, [(str(i),1) for i in range(15,-1,-1)], self),
                      Register(0x05, "REC_EN1",    0x0000, [(str(i),1) for i in range(31,15,-1)], self),
                      Register(0x06, "REC_EN2",    0x0000, [(str(i),1) for i in range(47,31,-1)], self),
                      Register(0x07, "REC_EN3",    0x0000, [(str(i),1) for i in range(63,47,-1)], self),
                      Register(0x08, "IMP_EN0",    0x0000, [(str(i),1) for i in range(15,-1,-1)], self),
                      Register(0x09, "IMP_EN1",    0x0000, [(str(i),1) for i in range(31,15,-1)], self),
                      Register(0x0A, "IMP_EN2",    0x0000, [(str(i),1) for i in range(47,31,-1)], self),
                      Register(0x0B, "IMP_EN3",    0x0000, [(str(i),1) for i in range(63,47,-1)], self),
                      Register(0x0C, "REC_CONFIG", 0x0000, [("CHOP_CLK",2),("CAP_GAIN",3),("RST_WIDTH",2),("",1),("REC_EN",1),("Z_MAG",3),("GM_RST",1),("EN_LDO",1),("SYNC_MODE",1),("WIDE_IN",1)], self),
                      Register(0x0D, "SYS_CONFIG", 0x0000, [("CLK_OUT_EN",1),("REC_STIM_BIAS",1),("REC_CURR_GEN",3),("BG_CLK",1),("BG_CAL",2),("IMP_CYCLES",4),("TX_DRIVE",4)], self),
                      Register(0x0E, "NULL",       0x0000, [("",16)], self, True),
                      Register(0x0F, "SCRATCH",    0x0000, [("SCRATCH",16)], self),
                      Register(0x10, "STIM_CFG0",  0x0000, [("NOCHECK",1),("BLK_ALL",1),("STIM_MULT",2),("STIM_AMP_B",6),("STIM_AMP_A",6)], self),
                      Register(0x11, "STIM_CFG1",  0x0000, [("STOP_MODE",1),("GND_RES",1),("PKG_PD",1),("REF_PD",1),("STIM_AMP_D",6),("STIM_AMP_C",6)], self),
                      Register(0x12, "STIM_CFG2",  0x0000, [("",1),("SHRT_TW_A",5),("IPH_GAPW_A",5),("PW_A",5)], self),
                      Register(0x13, "STIM_CFG3",  0x0000, [("",1),("SHRT_TW_B",5),("IPH_GAPW_B",5),("PW_B",5)], self),
                      Register(0x14, "STIM_CFG4",  0x0000, [("",1),("SHRT_TW_C",5),("IPH_GAPW_C",5),("PW_C",5)], self),
                      Register(0x15, "STIM_CFG5",  0x0000, [("",1),("SHRT_TW_D",5),("IPH_GAPW_D",5),("PW_D",5)], self),
                      Register(0x16, "STIM_CFG6",  0x0000, [("",1),("SW_C",5),("SW_B",5),("SW_A",5)], self),
                      Register(0x17, "STIM_CFG7",  0x0000, [("",1),("PKG_RET",1),("PCHGMOD",1),("CGND",1),("DOFF",1),("PR",1),("POL",1),("CL",2),("HRC",2),("SW_D",5)], self),
                      Register(0x18, "STIM_CFG8",  0x0000, [("",2),("NUMP_B",7),("NUMP_A",7)], self),
                      Register(0x19, "STIM_CFG9",  0x0000, [("",2),("NUMP_D",7),("NUMP_C",7)], self),
                      Register(0x1A, "STIM_CFG10", 0x0000, [("",1),("GMPULSE",1),("REGBIAS",1),("GMBIAS",1),("LOC2_A",6),("LOC1_A",6)], self),
                      Register(0x1B, "STIM_CFG11", 0x0000, [("",1),("STIMBIAS",3),("LOC2_B",6),("LOC1_B",6)], self),
                      Register(0x1C, "STIM_CFG12", 0x0000, [("",2),("TESTEN",1),("TESTSEL",1),("LOC2_C",6),("LOC1_C",6)], self),
                      Register(0x1D, "STIM_CFG13", 0x0000, [("",4),("LOC2_D",6),("LOC1_D",6)], self),
                      Register(0x1E, "STIM_CFG14", 0x0000, [("NCCP",6),("STIM_FREQ",10)], self),
                      Register(0x1F, "STIM_CFG15", 0x0000, [("",16)], self, True)
                    ]
*SENSE:Minimize
NAME          MODEL
ROWS
 N  OBJ
 L  C0000000
 G  C0000001
COLUMNS
    MARK      'MARKER'                 'INTORG'
    X0000000  OBJ       -2.094337685169e+01
    MARK      'MARKER'                 'INTEND'
    MARK      'MARKER'                 'INTORG'
    X0000001  OBJ       -4.258442129235e+00
    MARK      'MARKER'                 'INTEND'
    MARK      'MARKER'                 'INTORG'
    X0000002  OBJ       -1.506527754104e-02
    MARK      'MARKER'                 'INTEND'
    X0000003  C0000000  -1.666666666667e-03
    X0000003  C0000001  -1.666666666667e-03
    X0000003  OBJ       -1.333333333333e-01
RHS
    RHS       C0000000   5.846592582781e-01
    RHS       C0000001  -2.153407417219e-01
BOUNDS
 BV BND       X0000000
 BV BND       X0000001
 BV BND       X0000002
 LO BND       X0000003  -6.000000000000e+00
 UP BND       X0000003   6.000000000000e+00
ENDATA

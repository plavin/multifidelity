CREATE TABLE IF NOT EXISTS trace (
    trace_id           INTEGER   PRIMARY KEY,
   	benchmark          TEXT  NOT NULL,
	benchmark_options  TEXT,
    parrot_MHz         INTEGER   NOT NULL,
    trace_length       INTEGER   NOT NULL
);

CREATE TABLE IF NOT EXISTS pdsd ( /*phase detector/stability detector*/
    trace_id     INTEGER  NOT NULL,
    threshold    REAL NOT NULL,
    phase_length INTEGER  NOT NULL,
    stable_min   INTEGER  NOT NULL,
    window_start INTEGER  NOT NULL,
    summarize    INTEGER  NOT NULL,
    proj_dist    INTEGER  NOT NULL,
    proj_delta   REAL NOT NULL,
    p_j          INTEGER  NOT NULL,
    pct          REAL NOT NULL,
    error        REAL NOT NULL,
    PRIMARY KEY (trace_id, threshold, phase_length, stable_min, window_start, summarize, proj_dist, proj_delta, p_j),
    FOREIGN KEY (trace_id)
      REFERENCES trace (trace_id)
);

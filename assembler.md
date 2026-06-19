# CHIP-8 Assembler Architecture: Call Tree & Data Flow

```text
[ Main Script / __main__ ]
       │
       ▼
 1. cycle_with_file()  ◄─── (The Conductor: opens files and manages start/end)
       │
       ├───► 2. scan()  [Called in a Loop for each line of the .asm8 file]
       │         │
       │         └───► Populates: self.labels and self.scanned
       │
       ├───► 3. resolve() [Called ONCE after scanning finishes]
       │         │
       │         └───► Consumes: self.scanned ➔ Populates: self.resolved
       │
       └───► Encoding Loop [For each instruction inside self.resolved]:
                 │
                 ▼
           4. encode()
                 │
                 └───► 5. check_args() ◄─── (The Detective: parses and validates syntax)
                             │
                             ├───► Consumes: MNEMONIC_TABLE
                             │
                             └───► Returns: Matched Variant ➔ back to encode()

Assembler reads line by line and for each line:
      separete the coments post instruction. (ADD VX X ;Some comment)
      delate the coments
      cleans all ','
      ignore if its a clean line or just has coments
      create a label if its just "name": such as (my_label:)
      get the assembly instruction (ex: ADD VX Y)
      if the line has a insstrction (line[0]) and more (len(line) > 1) it get the args
      
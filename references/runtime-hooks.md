# Runtime Hooks: Evidence Before Patching

Dynamic hooks are high risk because static ROM models omit timing, memory ownership, DMA, VRAM bank state, and interpreter branches.

Before changing code, capture actual hook entry, interpreter cursor/token, selected record/coordinate system, source and destination addresses, upload completion, destination checksum after upload and before draw, and later bulk copies/clears/bank switches.

Do not conclude that a record is selected because it exists, a tile remains resident because it uploaded once, all paths hit a hook because offline cursors align, or rendering works because overlay checks pass.

Preserve registers, ABI, stack alignment, and replaced instructions. Prefer pointers captured while the decompressed resource base is known. Update overlay tables, BSS, and arena boundaries when code grows. Keep dynamic slots disjoint from state markers globally. Fail if records target controls, pages overflow, or a dynamic use lacks the latest mapping. Name outputs “test” until runtime evidence passes.

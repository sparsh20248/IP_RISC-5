
a:     file format pe-i386


Disassembly of section .text:

00000000 <_main>:
   0:	55                   	push   %ebp
   1:	89 e5                	mov    %esp,%ebp
   3:	83 e4 f0             	and    $0xfffffff0,%esp
   6:	83 ec 30             	sub    $0x30,%esp
   9:	e8 00 00 00 00       	call   e <_main+0xe>
   e:	c7 44 24 2c 05 00 00 	movl   $0x5,0x2c(%esp)
  15:	00 
  16:	c7 44 24 28 0f 00 00 	movl   $0xf,0x28(%esp)
  1d:	00 
  1e:	c7 44 24 24 10 00 00 	movl   $0x10,0x24(%esp)
  25:	00 
  26:	c7 44 24 20 ff ff ff 	movl   $0xffffffff,0x20(%esp)
  2d:	ff 
  2e:	c7 44 24 1c 03 00 00 	movl   $0x3,0x1c(%esp)
  35:	00 
  36:	c7 44 24 18 01 00 00 	movl   $0x1,0x18(%esp)
  3d:	00 
  3e:	c7 44 24 14 02 00 00 	movl   $0x2,0x14(%esp)
  45:	00 
  46:	8b 54 24 2c          	mov    0x2c(%esp),%edx
  4a:	8b 44 24 28          	mov    0x28(%esp),%eax
  4e:	01 d0                	add    %edx,%eax
  50:	89 44 24 10          	mov    %eax,0x10(%esp)
  54:	8b 44 24 2c          	mov    0x2c(%esp),%eax
  58:	2b 44 24 28          	sub    0x28(%esp),%eax
  5c:	89 44 24 0c          	mov    %eax,0xc(%esp)
  60:	8b 44 24 2c          	mov    0x2c(%esp),%eax
  64:	8d 50 ff             	lea    -0x1(%eax),%edx
  67:	89 54 24 2c          	mov    %edx,0x2c(%esp)
  6b:	85 c0                	test   %eax,%eax
  6d:	0f 95 c0             	setne  %al
  70:	84 c0                	test   %al,%al
  72:	74 02                	je     76 <_main+0x76>
  74:	eb ea                	jmp    60 <_main+0x60>
  76:	b8 00 00 00 00       	mov    $0x0,%eax
  7b:	c9                   	leave  
  7c:	c3                   	ret    
  7d:	90                   	nop
  7e:	90                   	nop
  7f:	90                   	nop

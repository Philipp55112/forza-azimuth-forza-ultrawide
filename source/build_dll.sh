set -e
clang --target=x86_64-pc-windows-msvc -ffreestanding -O2 -fno-stack-protector -mno-stack-arg-probe -fno-builtin -c dinput8_proxy.c -o px.obj
printf 'LIBRARY dinput8\nEXPORTS\nDirectInput8Create\n' > px.def
lld-link /dll /nodefaultlib /entry:DllMain /def:px.def /out:dinput8.dll px.obj k32.lib u32.lib


all:
	( cd ../sol_wrap; make lib )
	( cp ../sol_wrap/osx/Release/libsol_wrap.dylib lib )

test:
	./run_tests.sh

clean:
	$(RM) -f *.pyc

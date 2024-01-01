APP_NAME := $(shell basename $$(pwd))
COMPILER := g++
FLAGS    := -g -Wall -fdiagnostics-color=never -fno-diagnostics-show-caret -DARCH=\"$(shell uname -m)\" -fPIC
INCLUDES := -I. -Isrc/include -I/usr/share/mkspecs/linux-g++ -I/usr/include/qt -I/usr/include/qt/QtCore -I/usr/include/qt/QtGui -I/usr/include/qt/QtWidgets -I/usr/include
DEFINES  := -DQT_GUI_LIB -DQT_CORE_LIB -D_REENTRANT
LIBS     := -lGL -lGLU -lQt5Core -lQt5Gui -lQt5Widgets -lpng


MOCLIST  := $(patsubst src/include/%.h,build/%.moc.cpp,$(shell grep -l Q_OBJECT src/include/*.h))
UICLIST  := $(patsubst src/ui/%.ui,build/%.ui.h,$(wildcard src/ui/*.ui))
OBJLIST  := $(patsubst src/cpp/%.cpp,build/%.o,$(wildcard src/cpp/*.cpp)) $(patsubst build/%.moc.cpp,build/%.moc.o,$(MOCLIST))

all: $(APP_NAME)

.PHONY: test
.PHONY: distclean

%: %.cpp 
	@echo ""
	@echo "compiling $< ..."
	@$(COMPILER) $(FLAGS) $(DEFINES) $(INCLUDES) -o $@ $< $(LIBS)
	@echo ""
	@stat -c '%n      %s Bytes' $@
	@echo ""

%.o: %.cpp

.PRECIOUS: build/%.o build/%.moc.cpp build/%.ui.h


ifneq "$(MAKECMDGOALS)" "distclean"
ifneq "$(MAKECMDGOALS)" "test"
DUMMY := $(shell mkdir -p build)
sinclude .depend
endif
endif

$(APP_NAME): $(OBJLIST)
	@echo ""
	@echo "linking ..."
	@$(COMPILER) $(FLAGS) -o $(APP_NAME) $(OBJLIST) $(LIBS)
	@echo ""
	@stat -c '%n      %s Bytes' $@
	@echo ""


build/%.o: src/cpp/%.cpp
	@echo "compiling $< ..."
	@$(COMPILER) -c $(FLAGS) $(DEFINES) $(INCLUDES) -o $@ $<


build/%.moc.o: build/%.moc.cpp
	@echo "compiling $< ..."
	@$(COMPILER) -c $(FLAGS) $(DEFINES) $(INCLUDES) -o $@ $<


build/%.moc.cpp: src/include/%.h
	@echo "mocking   $< ..."
	@moc --no-notes $(DEFINES) $(INCLUDES) $< -o $@


build/%.ui.h: src/ui/%.ui build/%.moc.cpp
	@echo "UICing    $< ..."
	@uic $< -o $@

.depend: src/cpp/*.cpp src/include/*.h src/ui/*.ui
	@for f in src/cpp/*.cpp ; do k=$$(basename $$f); cpp $(FLAGS) $(DEFINES) $(INCLUDES) -M -MG -MT build/$${k%.*}.o $$f ; done > .depend

distclean:
	@rm -rfv .depend build $(APP_NAME)



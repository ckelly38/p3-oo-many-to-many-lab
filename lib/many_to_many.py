class Author:
    def __init__(self, nm):
        self.name = nm;

    def contracts(self):
        return [cntrc for cntrc in Contract.all if cntrc.author == self];

    def books(self):
        return [cntrc.book for cntrc in Contract.all if cntrc.author == self];

    def sign_contract(self, bk, dt, rfee):
        return Contract(self, bk, dt, rfee);

    def total_royalties(self):
        return sum([cntrc.royalties for cntrc in Contract.all if cntrc.author == self]);


class Book:
    def __init__(self, ttl):
        self.title = ttl;

    def contracts(self):
        return [cntrc for cntrc in Contract.all if cntrc.book == self];

    def authors(self):
        return [cntrc.author for cntrc in Contract.all if cntrc.book == self];


class Contract:
    all = [];

    def __init__(self, atr, bk, dt, rfee):
        self.setAuthor(atr);
        self.setBook(bk);
        self.setDate(dt);
        self.setRoyalties(rfee);
        Contract.all.append(self);

    def getDelimIndexes(self, val):
        if (type(val) == int):
            if (val == 10): return [[2, 5]];
            elif (val == 8): return [[1, 3]];
            elif (val == 9): return [[1, 4], [2, 4]];
            else: raise ValueError("length must be 8, 9, or 10 only!");
        else: raise Exception("invalid type found for the length it must be an integer!");

    def isLeapYear(self, val):
        if (val == None): raise Exception("a numeric value must be used here!");
        elif (type(val) == int): pass;
        else: raise Exception("a numeric value must be used here!");
        if (val % 400 == 0): return True;
        else:
            if (val % 100 == 0): return False;
            else:
                if (val % 4 == 0): return True;
                else: return False;

    def getMonthDayAndYearFromDateString(self, val):
        #print(f"isvaliddate val = {val}");
        if (val == None): return False;
        elif (len(val) < 8 or len(val) > 10): return False;
        #month day year
        #01/01/2001 len = 10
        #1/01/2001 len = 9
        #01/1/2001 len = 9
        #1/1/2001 len = 8
        #0123456789

        mydelimindxs = self.getDelimIndexes(len(val));
        myadelimindx = -1;
        mybdelimindx = -1;
        if (len(mydelimindxs) == 1):
            myadelimindx = mydelimindxs[0][0];
            mybdelimindx = mydelimindxs[0][1];
        elif (len(mydelimindxs) == 2):
            mybdelimindx = mydelimindxs[0][1];
            fdelimindx = val.index("/");
            if (fdelimindx < 0 or fdelimindx > len(val) - 1):
                fdelimindx = val.index("-");
            if (fdelimindx < 0 or fdelimindx > len(val) - 1):
                raise Exception("there must be a delimeter in the date string, but there was not!");
            myadelimindx = fdelimindx;
            if (myadelimindx == mydelimindxs[0][0] or myadelimindx == mydelimindxs[1][0]): pass;
            else: raise Exception("invalid delimeter index found and used here!");
        else: raise Exception("invalid length found and used for the delimeter indexes!");
        #print(f"myadelimindx = {myadelimindx}");
        #print(f"mybdelimindx = {mybdelimindx}");

        if (val[myadelimindx] == val[mybdelimindx] and
            (val[myadelimindx] == "/" or val[myadelimindx] == "-")): pass;
        else: return False;

        for i in range(len(val)):
            if (i == myadelimindx or i == mybdelimindx): continue;
            else:
                if (val[i].isnumeric()): pass;
                else: return False;
        #print("contains numbers at the correct spots!");

        monthnum = int(val[0:myadelimindx]);
        daynum = int(val[myadelimindx + 1:mybdelimindx]);
        yrnum = int(val[mybdelimindx + 1:]);
        #print(f"monthnum = {monthnum}");
        #print(f"daynum = {daynum}");
        #print(f"yrnum = {yrnum}");

        return (monthnum, daynum, yrnum);

    def isValidDate(self, val):
        datetpl = self.getMonthDayAndYearFromDateString(val);
        monthnum = datetpl[0];
        daynum = datetpl[1];
        yrnum = datetpl[2];

        if (monthnum < 1 or monthnum > 12): return False;
        if (daynum < 1 or daynum > 31): return False;
        if (yrnum < 1): return False;

        #30 days has September (9), April (4), June (6), and November (11);
        #all the rest have 31 except for February
        #February has 28 or 29 days normally (29 if leap year)

        monthswithtdydays = [4, 6, 9, 11];
        #monthswithtndydays = [i + 1 for i in range(12) if i + 1 != 2 and i + 1 not in monthswithtdydays];
        #print(f"monthswithtdydays = {monthswithtdydays}");
        #print(f"monthswithtndydays = {monthswithtndydays}");
        
        if (monthnum in monthswithtdydays and daynum > 30): return False;
        if (monthnum == 2):
            if (daynum > 29): return False;
            islpyr = self.isLeapYear(yrnum);
            #print(f"islpyr = {islpyr}");
            
            if (islpyr): pass;
            else:
                if (daynum > 28): return False;

        return True;

    def getAuthor(self): return self._author;

    def getDate(self): return self._date;
    
    def getBook(self): return self._book;
    
    def getRoyalties(self): return self._royalties;

    def setAuthorOrBookOrDateOrRoyalties(self, val, typestr):
        validtypes = ["author", "book", "date", "royalties"];
        if ((typestr == None) or (len(typestr) < 1) or (typestr.lower() not in validtypes)):
            raise Exception("invalid typestr passed in!");
        if (typestr.lower() == validtypes[0] and isinstance(val, Author)): self._author = val;
        elif (typestr.lower() == validtypes[1] and isinstance(val, Book)): self._book = val;
        elif (typestr.lower() == validtypes[2] and self.isValidDate(val)): self._date = val;
        elif (typestr.lower() == validtypes[3] and type(val) == int): self._royalties = val;
        else: raise Exception("invalid data type found and used here!");

    def setAuthor(self, val): self.setAuthorOrBookOrDateOrRoyalties(val, "author");
    
    def setBook(self, val): self.setAuthorOrBookOrDateOrRoyalties(val, "book");

    def setDate(self, val): self.setAuthorOrBookOrDateOrRoyalties(val, "date");
    
    def setRoyalties(self, val): self.setAuthorOrBookOrDateOrRoyalties(val, "royalties");

    def isDateABeforeDateB(self, vala, valb):
        mdyrtpla = self.getMonthDayAndYearFromDateString(vala);
        mdyrtplb = self.getMonthDayAndYearFromDateString(valb);
        #return value from above method is month, day, year
        #we want to check the values in year, month, day
        indxs = [2, 0, 1];
        for i in indxs:
            if (mdyrtpla[i] < mdyrtplb[i]): return True;
            elif (mdyrtplb[i] < mdyrtpla[i]): return False;
        #the dates are both equal, so a is not less than b
        return False;

    @classmethod
    def contracts_by_date(cls, val):
        return [cntrc for cntrc in Contract.all if cntrc.date == val];    

    author = property(getAuthor, setAuthor);

    book = property(getBook, setBook);

    date = property(getDate, setDate);

    royalties = property(getRoyalties, setRoyalties);

#atr = Author("Name");
#bk = Book("Title");
#mc = Contract(atr, bk, "02/29/2000", 0);

#pragma once

template<class T>
struct ClearType
{
	typedef T Type;
};

template<class T>
struct ClearType < T* >
{
	typedef T Type;
};

template<class T>
struct ClearType < T& >
{
	typedef T Type;
};

template<class To, class From>
class CanCast
{
	static char Can(To*);
	static int Can(...);
public:
	enum
	{
		Result = sizeof(Can((From*)0)) == sizeof(char)
	};

};
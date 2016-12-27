#pragma once

#include <functional>
#include <map>
#include "Tools.h"
using namespace std;

template<class Container>
class Serializable
{
protected:
	typedef function<void(const string&, Container&)> Func;

	struct SerializerPair
	{
		Func Serializer;
		Func Deserializer;
	};

	Container* ContainerInf = 0;
			
	Serializable() = default;
	Serializable(Serializable&) = default;
	Serializable& operator=(Serializable&) = default;
	~Serializable() = default;

	char Add(string _key, Func _serializer, Func _deserializer)
	{
		auto& lv_Pair = m_Serializers[_key]; 
		lv_Pair.Serializer = _serializer;
		lv_Pair.Deserializer = _deserializer;

		return 0;
	}

public:
	virtual void Serialize(Container& _cont)
	{
		for(auto& lv_Ser : m_Serializers)
			lv_Ser.second.Serializer(lv_Ser.first, _cont);
	}

	virtual void Deserialize(Container& _cont)
	{
		for (auto& lv_Ser : m_Serializers)
			lv_Ser.second.Deserializer(lv_Ser.first, _cont);
	}

private:
	
	map<string, SerializerPair> m_Serializers;
};

template<bool UNUSE>
struct SerializerEX
{};

template<>
struct SerializerEX < false >
{
	template<class T, class Cont, class UNUSE>
	void Serialize(const string& _key, T& _val, Cont& _cont, UNUSE)
	{
		::Serialize(_key, &_val, _cont);
	}

	template<class T, class Cont, class UNUSE>
	void Deserialize(const string& _key, T& _val, Cont& _cont, UNUSE)
	{
		::Deserialize(_key, &_val, _cont);
	}
};

template<>
struct SerializerEX < true >
{
	template<class T, class Cont, class UNUSE>
	void Serialize(const string& _key, T& _val, Cont& _cont, UNUSE)
	{
		::Serialize(_key, (UNUSE)&_val, _cont);
	}

	template<class T, class Cont, class UNUSE>
	void Deserialize(const string& _key, T& _val, Cont& _cont, UNUSE)
	{
		::Deserialize(_key, (UNUSE)&_val, _cont);
	}
};


#define UNNAMED_IMPL(x, y) UNNAMED_##x##_##y
#define UNNAMED_DECL(x, y) UNNAMED_IMPL(x, y)
#define UNNAMED UNNAMED_DECL(__LINE__ , __COUNTER__)

#define serialize(x) char UNNAMED = Add																	\
(																										\
	#x,																									\
	[this](const string& _key, ClearType<decltype(ContainerInf)>::Type& _cont)							\
	{																									\
		SerializerEX																					\
		<																								\
			CanCast																						\
			<																							\
				Serializable< ClearType<decltype(ContainerInf)>::Type >,								\
				ClearType<decltype(x)>::Type															\
			>::Result																					\
		> EX;																							\
		EX.Serialize(_key, x, _cont, (Serializable< ClearType<decltype(ContainerInf)>::Type >*)0);		\
	},																									\
																										\
	[this](const string& _key, ClearType<decltype(ContainerInf)>::Type& _cont) mutable					\
	{																									\
		SerializerEX																					\
		<																								\
			CanCast																						\
			<																							\
				Serializable< ClearType<decltype(ContainerInf)>::Type >,								\
				ClearType<decltype(x)>::Type															\
			>::Result																					\
		> EX;																							\
		EX.Deserialize(_key, x, _cont, (Serializable< ClearType<decltype(ContainerInf)>::Type >*)0);	\
	}																									\
)
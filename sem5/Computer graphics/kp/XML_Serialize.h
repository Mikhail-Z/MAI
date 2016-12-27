#pragma once
#include "Serialize.h"
#include "pugi_xml\pugixml.hpp"
#include <string>


template<class T>
void Serialize(const string& _key, T* _val, pugi::xml_node& _node)
{
	_node.append_child(_key.c_str()).append_attribute("value") = *_val;
}

template<class T>
void Serialize(const string& _key, map<string, T>* _val, pugi::xml_node& _node)
{
	auto lv_Node = _node.append_child(_key.c_str());
	for (auto lv_Val : *_val)
	{
		Serialize(lv_Val.first, &lv_Val.second, lv_Node);
	}
}

template<>
void Serialize(const string& _key, string* _val, pugi::xml_node& _node)
{
	_node.append_child(_key.c_str()).append_attribute("value") = _val->c_str();
}

template<>
void Serialize(const string& _key, Serializable<pugi::xml_node>* _val, pugi::xml_node& _node)
{
	_val->Serialize( _node.append_child( _key.c_str() ) );
}


template<class T>
void Deserialize(const string& _key, T* _val, const pugi::xml_node& _node)
{
	static_assert(false, "No Deserialize");
}

template<class T>
void Deserialize(const string& _key, map<string, T>* _val, pugi::xml_node& _node)
{
	auto lv_Node = _node.child(_key.c_str());
	for (auto lv_Val : lv_Node)
	{
		Deserialize(lv_Val.name(), &(*_val)[lv_Val.name()], lv_Node);
	}
}

template<>
void Deserialize(const string& _key, float* _val, const pugi::xml_node& _node)
{
	*_val = _node.child(_key.c_str()).attribute("value").as_float() ;
}

template<>
void Deserialize(const string& _key, string* _val, const pugi::xml_node& _node)
{
	*_val = _node.child(_key.c_str()).attribute("value").as_string();
}

template<>
void Deserialize(const string& _key, Serializable<pugi::xml_node>* _val, const pugi::xml_node& _node)
{
	_val->Deserialize(_node.child(_key.c_str() ) );
}
import React from 'react';
import { Button, Popconfirm, Table } from 'antd';

const ProductList: React.FC<{products: {name: string}[]; onDelete:(id:string)=>void}>= ({
    onDelete,
    products,
}) => {
    const columns = [
        {
            title: 'Name',
            dataIndex: 'name'
        },
        {
            title: 'Action',
            render(text:string, record:any) {
                return(
                    <Popconfirm title="Delete?" onConfirm={()=> onDelete(record.id)}>
                        <Button>Delete</Button>
                    </Popconfirm>
                );
            },
            
        },
    ];
    return <Table rowKey="id" dataSource={products} columns={columns}></Table>
};

export default ProductList;
